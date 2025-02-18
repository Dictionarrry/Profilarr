import React from 'react';
import {Plus, TestTube, Loader, Save, X, Trash, Check} from 'lucide-react';
import Modal from '@ui/Modal';
import {useArrModal} from '@hooks/useArrModal';
import DataSelectorModal from './DataSelectorModal';
import SyncModal from './SyncModal';

const ArrModal = ({isOpen, onClose, onSubmit, editingArr}) => {
    const {
        formData,
        availableData,
        tagInput,
        errors,
        isLoading,
        isTestingConnection,
        deleteConfirm,
        saveConfirm,
        testConfirm,
        isDataDrawerOpen,
        setIsDataDrawerOpen,
        setTagInput,
        handleInputChange,
        handleDataToggle,
        handleAddTag,
        handleRemoveTag,
        handleTagInputKeyDown,
        handleTestConnection,
        handleSubmit,
        handleDelete,
        showSyncConfirm,
        setShowSyncConfirm,
        handleManualSync,
        isInitialSyncing
    } = useArrModal({isOpen, onSubmit, editingArr});

    const arrTypes = [
        {value: 'radarr', label: 'Radarr'},
        {value: 'sonarr', label: 'Sonarr'}
    ];

    const syncMethods = [
        {value: 'manual', label: 'Manual'},
        {value: 'pull', label: 'On Pull'},
        {value: 'schedule', label: 'Scheduled'}
    ];

    // Ensure data_to_sync always has the required structure
    const safeSelectedData = {
        profiles: formData.data_to_sync?.profiles || [],
        customFormats: formData.data_to_sync?.customFormats || []
    };

    // Handle sync method change
    const handleSyncMethodChange = e => {
        const newMethod = e.target.value;
        handleInputChange({
            target: {
                id: 'sync_method',
                value: newMethod
            }
        });

        // Reset data_to_sync when switching to manual
        if (newMethod === 'manual') {
            handleInputChange({
                target: {
                    id: 'data_to_sync',
                    value: {profiles: [], customFormats: []}
                }
            });
        }
    };

    const inputClasses = errorKey =>
        `w-full px-3 py-2 text-sm rounded-lg border ${
            errors[errorKey]
                ? 'border-red-500'
                : 'border-gray-300 dark:border-gray-600'
        } bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 ${
            errors[errorKey]
                ? 'focus:ring-red-500 focus:border-red-500'
                : 'focus:ring-blue-500 focus:border-blue-500'
        } placeholder-gray-400 dark:placeholder-gray-500 transition-all`;

    return (
        <Modal
            isOpen={isOpen}
            onClose={onClose}
            title={editingArr ? 'Edit Arr' : 'Add New Arr'}
            width='3xl'
            height='4xl'
            footer={
                <div className='flex justify-end space-x-3'>
                    {editingArr && (
                        <button
                            type='button'
                            onClick={handleDelete}
                            className='flex items-center px-3 py-2 text-sm rounded-lg bg-red-600 hover:bg-red-700 text-white font-medium transition-colors'>
                            {deleteConfirm ? (
                                <>
                                    <Check className='w-3.5 h-3.5 mr-2' />
                                    Confirm Delete
                                </>
                            ) : (
                                <>
                                    <Trash className='w-3.5 h-3.5 mr-2' />
                                    Delete
                                </>
                            )}
                        </button>
                    )}

                    <button
                        type='button'
                        onClick={handleTestConnection}
                        disabled={
                            isTestingConnection ||
                            !formData.arrServer ||
                            !formData.apiKey
                        }
                        className='flex items-center px-3 py-2 text-sm rounded-lg bg-emerald-600 hover:bg-emerald-700 
                                     disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium transition-colors'>
                        {isTestingConnection ? (
                            <>
                                <Loader className='w-3.5 h-3.5 mr-2 animate-spin' />
                                Testing...
                            </>
                        ) : testConfirm ? (
                            <>
                                <Check className='w-3.5 h-3.5 mr-2' />
                                Confirm Test
                            </>
                        ) : (
                            <>
                                <TestTube className='w-3.5 h-3.5 mr-2' />
                                Test Connection
                            </>
                        )}
                    </button>

                    <button
                        type='submit'
                        form='arrForm'
                        className='flex items-center px-3 py-2 text-sm rounded-lg bg-blue-600 hover:bg-blue-700 
                                     text-white font-medium transition-colors'>
                        {saveConfirm ? (
                            <>
                                <Check className='w-3.5 h-3.5 mr-2' />
                                Confirm {editingArr ? 'Update' : 'Add'}
                            </>
                        ) : editingArr ? (
                            <>
                                <Save className='w-3.5 h-3.5 mr-2' />
                                Update
                            </>
                        ) : (
                            <>
                                <Plus className='w-3.5 h-3.5 mr-2' />
                                Add
                            </>
                        )}
                    </button>
                </div>
            }>
            <form id='arrForm' onSubmit={handleSubmit} className='space-y-4'>
                {/* Name Field */}
                <div className='space-y-1.5'>
                    <label
                        htmlFor='name'
                        className='text-xs font-medium text-gray-700 dark:text-gray-300'>
                        Name
                    </label>
                    <input
                        id='name'
                        value={formData.name}
                        onChange={handleInputChange}
                        className={inputClasses('name')}
                        placeholder='My App Instance'
                        required
                    />
                </div>

                {/* Testing Instance */}
                <div className='space-y-1.5'>
                    <div className='flex items-center justify-between'>
                        <label className='flex items-center space-x-2'>
                            <input
                                type='checkbox'
                                checked={formData.is_testing || false}
                                onChange={e =>
                                    handleInputChange({
                                        target: {
                                            id: 'is_testing',
                                            value: e.target.checked
                                        }
                                    })
                                }
                                className='rounded border-gray-300 text-blue-600 focus:ring-blue-500'
                            />
                            <span className='text-sm text-gray-700 dark:text-gray-300'>
                                Use For Testing
                            </span>
                        </label>
                        <span className='text-xs text-gray-500 dark:text-gray-400 max-w-md text-right'>
                            Use this app as an endpoint for regex / custom
                            format testing - only needed for development. Only
                            one testing instance can exist per app type
                            (Radarr/Sonarr)
                        </span>
                    </div>
                </div>

                {/* Type Field */}
                <div className='space-y-1.5'>
                    <label
                        htmlFor='type'
                        className='text-xs font-medium text-gray-700 dark:text-gray-300'>
                        Type
                    </label>
                    <select
                        id='type'
                        value={formData.type}
                        onChange={handleInputChange}
                        className={inputClasses('type')}
                        required>
                        {arrTypes.map(t => (
                            <option key={t.value} value={t.value}>
                                {t.label}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Tags Field */}
                <div className='space-y-1.5'>
                    <label
                        htmlFor='tags'
                        className='text-xs font-medium text-gray-700 dark:text-gray-300'>
                        Tags
                    </label>
                    <div className='flex flex-wrap gap-2 mb-2'>
                        {formData.tags.map((tag, index) => (
                            <span
                                key={index}
                                className='inline-flex items-center bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300 text-xs rounded px-2 py-1'>
                                {tag}
                                <button
                                    type='button'
                                    onClick={() => handleRemoveTag(tag)}
                                    className='ml-1 hover:text-blue-900 dark:hover:text-blue-200'>
                                    <X size={12} />
                                </button>
                            </span>
                        ))}
                    </div>
                    <div className='flex gap-2'>
                        <input
                            id='tagInput'
                            value={tagInput}
                            onChange={e => setTagInput(e.target.value)}
                            onKeyDown={handleTagInputKeyDown}
                            className={inputClasses('tagInput')}
                            placeholder='Enter tags...'
                        />
                        <button
                            type='button'
                            onClick={handleAddTag}
                            className='px-3 py-2 text-sm rounded-lg bg-blue-100 text-blue-600 hover:bg-blue-200
                                         dark:bg-blue-900 dark:text-blue-300 dark:hover:bg-blue-800
                                         font-medium transition-colors'>
                            Add
                        </button>
                    </div>
                </div>

                {/* Server URL Field */}
                <div className='space-y-1.5'>
                    <label
                        htmlFor='arrServer'
                        className='text-xs font-medium text-gray-700 dark:text-gray-300'>
                        Arr Server
                    </label>
                    <input
                        id='arrServer'
                        value={formData.arrServer}
                        onChange={handleInputChange}
                        className={inputClasses('arrServer')}
                        placeholder='http://localhost:7878'
                        required
                    />
                    {errors.arrServer && (
                        <p className='text-xs text-red-500 mt-1'>
                            {errors.arrServer}
                        </p>
                    )}
                </div>

                {/* API Key Field */}
                <div className='space-y-1.5'>
                    <label
                        htmlFor='apiKey'
                        className='text-xs font-medium text-gray-700 dark:text-gray-300'>
                        API Key
                    </label>
                    <input
                        type='password'
                        id='apiKey'
                        value={formData.apiKey}
                        onChange={handleInputChange}
                        className={inputClasses('apiKey')}
                        placeholder='Enter your API key'
                        required
                    />
                </div>

                {/* Sync Method Field */}
                <div className='space-y-1.5'>
                    <label
                        htmlFor='sync_method'
                        className='text-xs font-medium text-gray-700 dark:text-gray-300'>
                        Sync Method
                    </label>
                    <select
                        id='sync_method'
                        value={formData.sync_method}
                        onChange={handleSyncMethodChange}
                        className={inputClasses('sync_method')}
                        required>
                        {syncMethods.map(m => (
                            <option key={m.value} value={m.value}>
                                {m.label}
                            </option>
                        ))}
                    </select>
                </div>

                <div className='mt-2 text-xs text-gray-500 dark:text-gray-400 space-y-2 bg-gray-50 dark:bg-gray-800/50 p-3 rounded-lg'>
                    {formData.sync_method === 'manual' && (
                        <p>
                            Manual sync allows you to selectively import data
                            when changes occur in the source instance. You'll
                            need to manually select and import the data you want
                            to sync.
                        </p>
                    )}
                    {formData.sync_method === 'pull' && (
                        <p>
                            On Pull automatically syncs data whenever the
                            database pulls in new changes. This is a "set and
                            forget" option - perfect for maintaining consistency
                            across instances without manual intervention.
                        </p>
                    )}
                    {formData.sync_method === 'schedule' && (
                        <p>
                            Scheduled sync runs at fixed intervals, ensuring
                            your instances stay in sync at regular times.
                        </p>
                    )}
                </div>

                {/* Import as Unique - Now always visible */}
                <div className='space-y-1.5'>
                    <div className='flex items-center justify-between'>
                        <label className='flex items-center space-x-2'>
                            <input
                                type='checkbox'
                                checked={formData.import_as_unique || false}
                                onChange={e =>
                                    handleInputChange({
                                        target: {
                                            id: 'import_as_unique',
                                            value: e.target.checked
                                        }
                                    })
                                }
                                className='rounded border-gray-300 text-blue-600 focus:ring-blue-500'
                            />
                            <span className='text-sm text-gray-700 dark:text-gray-300'>
                                Import as Unique
                            </span>
                        </label>
                        <span className='text-xs text-gray-500 dark:text-gray-400 max-w-sm text-right'>
                            Creates a unique hash from the data and target
                            instance name, allowing the same profile/format to
                            be imported multiple times
                        </span>
                    </div>
                </div>

                {/* Conditional Fields for Sync Method */}
                {formData.sync_method === 'schedule' && (
                    <div className='space-y-1.5'>
                        <label
                            htmlFor='sync_interval'
                            className='text-xs font-medium text-gray-700 dark:text-gray-300'>
                            Sync Interval (minutes)
                        </label>
                        <input
                            type='number'
                            id='sync_interval'
                            value={formData.sync_interval}
                            onChange={handleInputChange}
                            className={inputClasses('sync_interval')}
                            placeholder='Enter interval in minutes'
                            min='1'
                            required
                        />
                        {errors.sync_interval && (
                            <p className='text-xs text-red-500 mt-1'>
                                {errors.sync_interval}
                            </p>
                        )}
                    </div>
                )}

                {/* Sync Options */}
                {formData.sync_method !== 'manual' && (
                    <>
                        <button
                            type='button'
                            onClick={() => setIsDataDrawerOpen(true)}
                            className='w-full px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 
                                        bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700
                                        rounded-lg transition-colors
                                        border border-gray-200 dark:border-gray-700'>
                            <div className='flex flex-col space-y-2'>
                                <div className='flex items-center justify-between'>
                                    <span>Select Data to Sync</span>
                                </div>
                                {(safeSelectedData.profiles.length > 0 ||
                                    safeSelectedData.customFormats.length >
                                        0) && (
                                    <div className='flex flex-wrap gap-2'>
                                        {safeSelectedData.profiles.map(
                                            profile => (
                                                <span
                                                    key={profile}
                                                    className='inline-flex items-center bg-blue-100 text-blue-800 
                                                        dark:bg-blue-900 dark:text-blue-300 
                                                        text-xs rounded px-2 py-1'>
                                                    {profile}
                                                </span>
                                            )
                                        )}
                                        {safeSelectedData.customFormats.map(
                                            format => (
                                                <span
                                                    key={format}
                                                    className='inline-flex items-center bg-green-100 text-green-800 
                                                        dark:bg-green-900 dark:text-green-300 
                                                        text-xs rounded px-2 py-1'>
                                                    {format}
                                                </span>
                                            )
                                        )}
                                    </div>
                                )}
                            </div>
                        </button>

                        {errors.data_to_sync && (
                            <p className='text-xs text-red-500 mt-1'>
                                {errors.data_to_sync}
                            </p>
                        )}
                    </>
                )}

                <DataSelectorModal
                    isOpen={
                        formData.sync_method !== 'manual' && isDataDrawerOpen
                    }
                    onClose={() => setIsDataDrawerOpen(false)}
                    isLoading={isLoading}
                    availableData={availableData}
                    selectedData={safeSelectedData}
                    onDataToggle={handleDataToggle}
                    error={errors.data_to_sync}
                />
                {showSyncConfirm && (
                    <SyncModal
                        isOpen={showSyncConfirm}
                        onClose={() => {
                            setShowSyncConfirm(false);
                            onSubmit();
                        }}
                        onSkip={() => {
                            setShowSyncConfirm(false);
                            onSubmit();
                        }}
                        onSync={handleManualSync}
                        isSyncing={isInitialSyncing}
                    />
                )}
            </form>
        </Modal>
    );
};

export default ArrModal;
