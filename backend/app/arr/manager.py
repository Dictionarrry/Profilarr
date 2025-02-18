# arr/manager.py

from ..db import get_db
import json
import logging

# Import our task-utils that handle DB insertion for scheduled tasks
from .task_utils import (create_import_task_for_arr_config,
                         update_import_task_for_arr_config,
                         delete_import_task_for_arr_config)

from ..task.tasks import TaskScheduler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def save_arr_config(config):
    """
    Create a new arr_config row, then create a corresponding scheduled task (if sync_method != manual).
    Store the newly created task's ID in arr_config.import_task_id.
    
    If is_testing is True, ensures only one testing instance exists per arr type.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            # Check if name already exists
            existing = cursor.execute(
                'SELECT id FROM arr_config WHERE name = ?',
                (config['name'], )).fetchone()

            if existing:
                logger.warning(
                    f"[save_arr_config] Attempted to create duplicate config name: {config['name']}"
                )
                return {
                    'success': False,
                    'error': 'Configuration with this name already exists',
                    'status_code': 409
                }

            # Check if there's already a testing instance for this arr type
            if config.get('is_testing'):
                existing_testing = cursor.execute(
                    'SELECT id, name FROM arr_config WHERE type = ? AND is_testing = 1',
                    (config['type'], )).fetchone()

                if existing_testing:
                    logger.warning(
                        f"[save_arr_config] Attempted to create second testing instance for {config['type']}"
                    )
                    return {
                        'success': False,
                        'error':
                        f"A testing instance already exists for {config['type']} ('{existing_testing['name']}')",
                        'status_code': 409
                    }

            # 1) Insert the arr_config row
            logger.debug(
                f"[save_arr_config] Attempting to create new arr_config with name={config['name']} sync_method={config.get('sync_method')}"
            )

            cursor.execute(
                '''
                INSERT INTO arr_config (
                    name, type, tags, arr_server, api_key, 
                    data_to_sync, last_sync_time, sync_percentage,
                    sync_method, sync_interval, import_as_unique,
                    import_task_id, is_testing
                )
                VALUES (?, ?, ?, ?, ?, ?, NULL, 0, ?, ?, ?, NULL, ?)
                ''', (
                    config['name'],
                    config['type'],
                    json.dumps(config.get('tags', [])),
                    config['arrServer'],
                    config['apiKey'],
                    json.dumps(config.get('data_to_sync', {})),
                    config.get('sync_method', 'manual'),
                    config.get('sync_interval', 0),
                    config.get('import_as_unique', False),
                    config.get('is_testing', False),
                ))
            conn.commit()

            new_config_id = cursor.lastrowid
            logger.info(
                f"[save_arr_config] Created new arr_config row #{new_config_id} for '{config['name']}'"
            )

            # 2) Create a scheduled task row if needed
            sync_method = config.get('sync_method', 'manual')
            sync_interval = config.get('sync_interval', 0)
            task_id = create_import_task_for_arr_config(
                config_id=new_config_id,
                config_name=config['name'],
                sync_method=sync_method,
                sync_interval=sync_interval)

            # 3) Update arr_config.import_task_id if a task was created
            if task_id:
                logger.debug(
                    f"[save_arr_config] Updating arr_config #{new_config_id} with import_task_id={task_id}"
                )
                cursor.execute(
                    'UPDATE arr_config SET import_task_id = ? WHERE id = ?',
                    (task_id, new_config_id))
                conn.commit()

            scheduler = TaskScheduler.get_instance()
            if scheduler:
                logger.debug("[save_arr_config] Reloading tasks from DB...")
                scheduler.load_tasks_from_db()

            return {'success': True, 'id': new_config_id}

        except Exception as e:
            logger.error(
                f"[save_arr_config] Error saving arr config: {str(e)}")
            return {'success': False, 'error': str(e)}


def update_arr_config(id, config):
    """
    Update an existing arr_config row.
    If is_testing is being enabled, ensures only one testing instance exists per arr type.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            # Check if name already exists (excluding current config)
            existing = cursor.execute(
                'SELECT id FROM arr_config WHERE name = ? AND id != ?',
                (config['name'], id)).fetchone()

            if existing:
                logger.warning(
                    f"[update_arr_config] Attempted to update config #{id} to duplicate name: {config['name']}"
                )
                return {
                    'success': False,
                    'error': 'Configuration with this name already exists',
                    'status_code': 409
                }

            # If enabling testing mode, check for existing testing instance
            if config.get('is_testing'):
                existing_testing = cursor.execute(
                    'SELECT id, name FROM arr_config WHERE type = ? AND is_testing = 1 AND id != ?',
                    (config['type'], id)).fetchone()

                if existing_testing:
                    logger.warning(
                        f"[update_arr_config] Attempted to create second testing instance for {config['type']}"
                    )
                    return {
                        'success': False,
                        'error':
                        f"A testing instance already exists for {config['type']} ('{existing_testing['name']}')",
                        'status_code': 409
                    }

            # 1) Grab existing row so we know the existing import_task_id
            existing_row = cursor.execute(
                'SELECT * FROM arr_config WHERE id = ?', (id, )).fetchone()
            if not existing_row:
                logger.debug(
                    f"[update_arr_config] No arr_config row found with id={id}"
                )
                return {'success': False, 'error': 'Configuration not found'}

            existing_task_id = existing_row['import_task_id']

            # 2) Update the arr_config row itself
            logger.debug(
                f"[update_arr_config] Updating arr_config #{id} name={config['name']} sync_method={config.get('sync_method')}"
            )

            cursor.execute(
                '''
                UPDATE arr_config
                SET name = ?,
                    type = ?,
                    tags = ?,
                    arr_server = ?,
                    api_key = ?,
                    data_to_sync = ?,
                    sync_method = ?,
                    sync_interval = ?,
                    import_as_unique = ?,
                    is_testing = ?
                WHERE id = ?
                ''',
                (config['name'], config['type'],
                 json.dumps(config.get('tags', [])), config['arrServer'],
                 config['apiKey'], json.dumps(config.get(
                     'data_to_sync', {})), config.get('sync_method', 'manual'),
                 config.get('sync_interval',
                            0), config.get('import_as_unique', False),
                 config.get('is_testing', False), id))
            conn.commit()
            if cursor.rowcount == 0:
                logger.debug(
                    f"[update_arr_config] arr_config #{id} not found for update"
                )
                return {'success': False, 'error': 'Configuration not found'}

            logger.info(f"[update_arr_config] Updated arr_config row #{id}")

            # 3) Create/Update/Remove the scheduled task row
            new_task_id = update_import_task_for_arr_config(
                config_id=id,
                config_name=config['name'],
                sync_method=config.get('sync_method', 'manual'),
                sync_interval=config.get('sync_interval', 0),
                existing_task_id=existing_task_id)

            # 4) Store new_task_id in arr_config.import_task_id
            logger.debug(
                f"[update_arr_config] Setting arr_config #{id} import_task_id to {new_task_id}"
            )
            cursor.execute(
                'UPDATE arr_config SET import_task_id = ? WHERE id = ?',
                (new_task_id, id))
            conn.commit()

            scheduler = TaskScheduler.get_instance()
            if scheduler:
                logger.debug("[update_arr_config] Reloading tasks from DB...")
                scheduler.load_tasks_from_db()

            return {'success': True}

        except Exception as e:
            logger.error(
                f"[update_arr_config] Error updating arr config: {str(e)}")
            return {'success': False, 'error': str(e)}


def delete_arr_config(id):
    """
    Delete an arr_config row, plus remove its scheduled_task if any.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            # 1) Fetch the row so we know which task to remove
            existing_row = cursor.execute(
                'SELECT * FROM arr_config WHERE id = ?', (id, )).fetchone()
            if not existing_row:
                logger.debug(
                    f"[delete_arr_config] No arr_config row found with id={id}"
                )
                return {'success': False, 'error': 'Configuration not found'}

            existing_task_id = existing_row['import_task_id']

            # 2) Delete the arr_config
            logger.debug(f"[delete_arr_config] Removing arr_config #{id}")
            cursor.execute('DELETE FROM arr_config WHERE id = ?', (id, ))
            conn.commit()
            if cursor.rowcount == 0:
                logger.debug(
                    f"[delete_arr_config] arr_config #{id} not found for deletion"
                )
                return {'success': False, 'error': 'Configuration not found'}

            logger.info(f"[delete_arr_config] Deleted arr_config #{id}")

            # 3) If there's a scheduled task, remove it
            if existing_task_id:
                delete_import_task_for_arr_config(existing_task_id,
                                                  config_id=id)

            scheduler = TaskScheduler.get_instance()
            if scheduler:
                logger.debug("[delete_arr_config] Reloading tasks from DB...")
                scheduler.load_tasks_from_db()

            return {'success': True}

        except Exception as e:
            logger.error(
                f"[delete_arr_config] Error deleting arr config: {str(e)}")
            return {'success': False, 'error': str(e)}


def get_all_arr_configs():
    with get_db() as conn:
        cursor = conn.execute('SELECT * FROM arr_config')
        rows = cursor.fetchall()
        try:
            configs = []
            for row in rows:
                configs.append({
                    'id':
                    row['id'],
                    'name':
                    row['name'],
                    'type':
                    row['type'],
                    'tags':
                    json.loads(row['tags']) if row['tags'] else [],
                    'arrServer':
                    row['arr_server'],
                    'apiKey':
                    row['api_key'],
                    'data_to_sync': (json.loads(row['data_to_sync'])
                                     if row['data_to_sync'] else {}),
                    'last_sync_time':
                    row['last_sync_time'],
                    'sync_percentage':
                    row['sync_percentage'],
                    'sync_method':
                    row['sync_method'],
                    'sync_interval':
                    row['sync_interval'],
                    'import_as_unique':
                    bool(row['import_as_unique']),
                    'import_task_id':
                    row['import_task_id'],
                    'is_testing':
                    bool(row['is_testing'])
                })
            return {'success': True, 'data': configs}
        except Exception as e:
            logger.error(f"[get_all_arr_configs] Error: {str(e)}")
            return {'success': False, 'error': str(e)}


def get_arr_config(id):
    with get_db() as conn:
        cursor = conn.execute('SELECT * FROM arr_config WHERE id = ?', (id, ))
        row = cursor.fetchone()
        try:
            if row:
                return {
                    'success': True,
                    'data': {
                        'id':
                        row['id'],
                        'name':
                        row['name'],
                        'type':
                        row['type'],
                        'tags':
                        json.loads(row['tags']) if row['tags'] else [],
                        'arrServer':
                        row['arr_server'],
                        'apiKey':
                        row['api_key'],
                        'data_to_sync': (json.loads(row['data_to_sync'])
                                         if row['data_to_sync'] else {}),
                        'last_sync_time':
                        row['last_sync_time'],
                        'sync_percentage':
                        row['sync_percentage'],
                        'sync_method':
                        row['sync_method'],
                        'sync_interval':
                        row['sync_interval'],
                        'import_as_unique':
                        bool(row['import_as_unique']),
                        'import_task_id':
                        row['import_task_id'],
                        'is_testing':
                        bool(row['is_testing'])
                    }
                }
            logger.debug(
                f"[get_arr_config] No arr_config row found with id={id}")
            return {'success': False, 'error': 'Configuration not found'}
        except Exception as e:
            logger.error(f"[get_arr_config] Error: {str(e)}")
            return {'success': False, 'error': str(e)}


def get_scheduled_configs():
    """
    Return all arr_configs where sync_method='schedule'.
    Potentially used if you want to see scheduled ones explicitly.
    """
    with get_db() as conn:
        cursor = conn.execute('SELECT * FROM arr_config WHERE sync_method = ?',
                              ('schedule', ))
        rows = cursor.fetchall()
        try:
            configs = []
            for row in rows:
                configs.append({
                    'id': row['id'],
                    'name': row['name'],
                    'sync_interval': row['sync_interval'],
                    'import_task_id': row['import_task_id']
                })
            return {'success': True, 'data': configs}
        except Exception as e:
            logger.error(f"[get_scheduled_configs] Error: {str(e)}")
            return {'success': False, 'error': str(e)}


def get_pull_configs():
    with get_db() as conn:
        rows = conn.execute(
            'SELECT * FROM arr_config WHERE sync_method = "pull"').fetchall()

        results = []
        for row in rows:
            results.append({
                'id':
                row['id'],
                'name':
                row['name'],
                'type':
                row['type'],
                'tags':
                json.loads(row['tags']) if row['tags'] else [],
                'arrServer':
                row['arr_server'],
                'apiKey':
                row['api_key'],
                'data_to_sync': (json.loads(row['data_to_sync'])
                                 if row['data_to_sync'] else {}),
                'last_sync_time':
                row['last_sync_time'],
                'sync_percentage':
                row['sync_percentage'],
                'sync_method':
                row['sync_method'],
                'sync_interval':
                row['sync_interval'],
                'import_as_unique':
                bool(row['import_as_unique']),
                'import_task_id':
                row['import_task_id'],
                'is_testing':
                bool(row['is_testing'])
            })
        return results


def run_import_for_config(config_row):
    """
    Perform the same import logic as the /import endpoints, but automatically
    for a "pull-based" or "schedule-based" ARR config.

    Calculates sync percentage based on explicitly selected items only:
    - Each selected profile counts as 1
    - Each selected custom format counts as 1
    """
    from datetime import datetime
    from ..db import get_db

    arr_id = config_row['id']
    arr_name = config_row['name']
    arr_type = config_row['type']
    arr_server = config_row['arrServer']
    api_key = config_row['apiKey']
    import_as_unique = config_row.get('import_as_unique', False)

    logger.info(
        f"[Pull Import] Running import for ARR config #{arr_id} ({arr_name})")

    # Safely parse data_to_sync
    data_to_sync = config_row['data_to_sync'] or {}

    selected_profiles = data_to_sync.get('profiles', [])
    selected_formats = data_to_sync.get('customFormats', [])

    # Log import_as_unique setting
    if import_as_unique:
        logger.info(f"Unique imports for {arr_name} are on, adjusting names")
    else:
        logger.info(
            f"Unique imports for {arr_name} are off, using original names")

    # Calculate total_attempted based on explicitly selected items only
    total_attempted = len(selected_formats) + len(selected_profiles)
    total_successful = 0

    # 1) Import user-selected custom formats (counting these in percentage)
    if selected_formats:
        logger.info(
            f"[Pull Import] Importing {len(selected_formats)} user-selected CFs for ARR #{arr_id}"
        )
        try:
            from ..importarr.format import import_formats_to_arr
            format_names = selected_formats
            original_names = format_names.copy()

            # Modify format names if import_as_unique is true
            if import_as_unique:
                format_names = [
                    f"{name} [Dictionarry]" for name in format_names
                ]
                logger.info(
                    f"Modified format names for unique import: {format_names}")

            format_result = import_formats_to_arr(
                format_names=format_names,
                original_names=original_names,
                base_url=arr_server,
                api_key=api_key,
                arr_type=arr_type)

            if format_result.get('success'):
                total_successful += (format_result.get('added', 0) +
                                     format_result.get('updated', 0))
            else:
                logger.warning(
                    f"[Pull Import] Importing user-selected CFs for ARR #{arr_id} had errors: {format_result}"
                )
        except Exception as e:
            logger.exception(
                f"[Pull Import] Failed importing user-selected CFs for ARR #{arr_id}: {str(e)}"
            )

    # 2) For user-selected profiles, gather any referenced CFs
    referenced_cf_names = set()
    if selected_profiles:
        from pathlib import Path
        from ..data.utils import get_category_directory, load_yaml_file

        for profile_name in selected_profiles:
            try:
                profile_file = Path(
                    get_category_directory('profile')) / f"{profile_name}.yml"
                if not profile_file.exists():
                    logger.error(
                        f"[Pull Import] Profile file not found: {profile_file}"
                    )
                    continue

                profile_data = load_yaml_file(str(profile_file))
                for cf in profile_data.get('custom_formats', []):
                    if 'name' in cf:
                        referenced_cf_names.add(cf['name'])
            except Exception as e:
                logger.error(
                    f"[Pull Import] Error loading profile {profile_name}: {str(e)}"
                )

    # Import referenced CFs
    if referenced_cf_names:
        try:
            from ..importarr.format import import_formats_to_arr
            format_names = list(referenced_cf_names)
            original_names = format_names.copy()

            # Modify format names if import_as_unique is true
            if import_as_unique:
                format_names = [
                    f"{name} [Dictionarry]" for name in format_names
                ]
                logger.info(
                    f"Modified format names for unique import: {format_names}")

            cf_result = import_formats_to_arr(format_names=format_names,
                                              original_names=original_names,
                                              base_url=arr_server,
                                              api_key=api_key,
                                              arr_type=arr_type)

            if not cf_result.get('success'):
                logger.warning(
                    f"[Pull Import] Importing referenced CFs had errors: {cf_result}"
                )
        except Exception as e:
            logger.exception(
                f"[Pull Import] Failed importing referenced CFs: {str(e)}")

    # 3) Import the profiles themselves
    if selected_profiles:
        try:
            from ..importarr.profile import import_profiles_to_arr
            profile_names = selected_profiles
            original_names = profile_names.copy()

            # Modify profile names if import_as_unique is true
            if import_as_unique:
                profile_names = [
                    f"{name} [Dictionarry]" for name in profile_names
                ]
                logger.info(
                    f"Modified profile names for unique import: {profile_names}"
                )

            profile_result = import_profiles_to_arr(
                profile_names=profile_names,
                original_names=original_names,
                base_url=arr_server,
                api_key=api_key,
                arr_type=arr_type,
                arr_id=arr_id,
                import_as_unique=import_as_unique)

            if profile_result.get('success'):
                # Count successful profile imports in total
                total_successful += (profile_result.get('added', 0) +
                                     profile_result.get('updated', 0))
            else:
                logger.warning(
                    f"[Pull Import] Importing profiles had errors: {profile_result}"
                )
        except Exception as e:
            logger.exception(
                f"[Pull Import] Failed importing profiles: {str(e)}")

    # Calculate percentage based on successful imports vs attempted
    sync_percentage = int((total_successful / total_attempted *
                           100) if total_attempted > 0 else 0)

    logger.info(
        f"[Pull Import] Done importing for ARR config #{arr_id} ({arr_name}). "
        f"Success rate: {total_successful}/{total_attempted} => {sync_percentage}%"
    )

    # Update arr_config with results
    now = datetime.now()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE arr_config
            SET last_sync_time = ?,
                sync_percentage = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''', (now, sync_percentage, arr_id))
        conn.commit()

    logger.info(
        f"[Pull Import] Updated ARR config #{arr_id} last_sync_time={now} & sync_percentage={sync_percentage}."
    )

    return {
        'success': True if total_successful > 0 else False,
        'total_attempted': total_attempted,
        'total_successful': total_successful,
        'sync_percentage': sync_percentage
    }


def check_active_sync_configs():
    """
    Check if there are any ARR configurations with non-manual sync methods.
    Returns (has_active_configs, details) tuple.
    """
    with get_db() as conn:
        cursor = conn.execute('''
            SELECT id, name, sync_method, data_to_sync 
            FROM arr_config 
            WHERE sync_method != 'manual'
        ''')
        active_configs = cursor.fetchall()

        if not active_configs:
            return False, None

        details = []
        for config in active_configs:
            data_to_sync = json.loads(
                config['data_to_sync'] if config['data_to_sync'] else '{}')
            if data_to_sync.get('profiles') or data_to_sync.get(
                    'customFormats'):
                details.append({
                    'id': config['id'],
                    'name': config['name'],
                    'sync_method': config['sync_method'],
                    'data': data_to_sync
                })

        return bool(details), details
