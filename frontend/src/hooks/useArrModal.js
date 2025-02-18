// useArrModal.js
import {useState, useEffect} from 'react';
import {
    pingService,
    saveArrConfig,
    updateArrConfig,
    deleteArrConfig,
    triggerSync
} from '@api/arr';
import {Profiles, CustomFormats} from '@api/data';
import Alert from '@ui/Alert';

export const useArrModal = ({isOpen, onSubmit, editingArr}) => {
    const [formData, setFormData] = useState({
        name: '',
        type: 'radarr',
        tags: [],
        arrServer: '',
        apiKey: '',
        sync_method: 'manual',
        sync_interval: 0,
        import_as_unique: false,
        is_testing: false,
        data_to_sync: {
            profiles: [],
            customFormats: []
        }
    });

    const [availableData, setAvailableData] = useState({
        profiles: [],
        customFormats: []
    });

    const [tagInput, setTagInput] = useState('');
    const [errors, setErrors] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const [isTestingConnection, setIsTestingConnection] = useState(false);
    const [deleteConfirm, setDeleteConfirm] = useState(false);
    const [saveConfirm, setSaveConfirm] = useState(false);
    const [testConfirm, setTestConfirm] = useState(false);
    const [isDataDrawerOpen, setIsDataDrawerOpen] = useState(false);
    const [showSyncConfirm, setShowSyncConfirm] = useState(false);
    const [isInitialSyncing, setIsInitialSyncing] = useState(false);
    const [syncConfigId, setSyncConfigId] = useState(null);

    useEffect(() => {
        if (editingArr) {
            setFormData({
                ...editingArr,
                import_as_unique: editingArr?.import_as_unique || false,
                is_testing: editingArr?.is_testing || false,
                data_to_sync: editingArr.data_to_sync || {
                    profiles: [],
                    customFormats: []
                }
            });
        } else {
            setFormData({
                name: '',
                type: 'radarr',
                tags: [],
                arrServer: '',
                apiKey: '',
                sync_method: 'manual',
                sync_interval: 0,
                import_as_unique: false,
                is_testing: false,
                data_to_sync: {
                    profiles: [],
                    customFormats: []
                }
            });
        }
        setTagInput('');
        setErrors({});
        setDeleteConfirm(false);
        setSaveConfirm(false);
        setTestConfirm(false);
        setIsDataDrawerOpen(false);
        setSyncConfigId(null);
    }, [editingArr]);

    // Close drawer when switching to manual sync
    useEffect(() => {
        if (formData.sync_method === 'manual') {
            setIsDataDrawerOpen(false);
        }
    }, [formData.sync_method]);

    useEffect(() => {
        if (isOpen && formData.sync_method !== 'manual') {
            fetchAvailableData();
        }
    }, [isOpen, formData.sync_method]);

    const validateUrl = url => {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    };

    const validateForm = () => {
        const newErrors = {};

        if (formData.arrServer && !validateUrl(formData.arrServer)) {
            newErrors.arrServer =
                'Please enter a valid URL (e.g., http://localhost:7878)';
        }

        if (
            formData.sync_method === 'schedule' &&
            (!formData.sync_interval || formData.sync_interval < 1)
        ) {
            newErrors.sync_interval =
                'Please enter a valid interval (minimum 1 minute)';
        }

        // Safely check data_to_sync structure
        if (formData.sync_method !== 'manual') {
            const profiles = formData.data_to_sync?.profiles || [];
            const customFormats = formData.data_to_sync?.customFormats || [];

            if (profiles.length === 0 && customFormats.length === 0) {
                newErrors.data_to_sync =
                    'Please select at least one profile or custom format to sync';
            }
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const fetchAvailableData = async () => {
        setIsLoading(true);
        try {
            const [profilesResponse, formatsResponse] = await Promise.all([
                Profiles.getAll(),
                CustomFormats.getAll()
            ]);

            setAvailableData({
                profiles: profilesResponse || [],
                customFormats: formatsResponse || []
            });
        } catch (error) {
            console.error('Error fetching data:', error);
            Alert.error('Failed to load sync data');
        } finally {
            setIsLoading(false);
        }
    };

    const handleTestConnection = async () => {
        if (!validateForm()) return;
        if (testConfirm) {
            setIsTestingConnection(true);
            try {
                const result = await pingService(
                    formData.arrServer,
                    formData.apiKey,
                    formData.type
                );
                if (result.success) {
                    Alert.success('Connection successful!');
                } else {
                    const message = result.message.includes('version')
                        ? `Unsupported ${formData.type} version. ${result.message}`
                        : `Connection failed: ${result.message}`;
                    Alert.error(message);
                }
            } catch (error) {
                Alert.error('An error occurred while testing the connection.');
            } finally {
                setIsTestingConnection(false);
                setTestConfirm(false);
            }
        } else {
            setTestConfirm(true);
            setTimeout(() => setTestConfirm(false), 3000);
        }
    };

    const handleSubmit = async e => {
        e.preventDefault();
        if (!validateForm()) return;

        if (saveConfirm) {
            try {
                const testResult = await pingService(
                    formData.arrServer,
                    formData.apiKey,
                    formData.type
                );
                if (!testResult.success) {
                    const message = testResult.message.includes('version')
                        ? `Unsupported ${formData.type} version. ${testResult.message}`
                        : `Connection test failed: ${testResult.message}`;
                    Alert.error(message);
                    setSaveConfirm(false);
                    return;
                }

                const configToSave = {
                    ...formData,
                    data_to_sync:
                        formData.sync_method === 'manual'
                            ? {}
                            : formData.data_to_sync
                };

                const saveResult = editingArr
                    ? await updateArrConfig(editingArr.id, configToSave)
                    : await saveArrConfig(configToSave);

                if (!saveResult.success) {
                    Alert.error(saveResult.error);
                    setSaveConfirm(false);
                    return;
                }

                Alert.success(
                    `Configuration ${
                        editingArr ? 'updated' : 'saved'
                    } successfully`
                );

                // If it's not a manual sync method, show the sync confirmation
                if (formData.sync_method !== 'manual') {
                    setSyncConfigId(editingArr ? editingArr.id : saveResult.id);
                    setShowSyncConfirm(true);
                } else {
                    onSubmit();
                }
            } catch (error) {
                Alert.error('Failed to save configuration');
                onSubmit();
            }
            setSaveConfirm(false);
        } else {
            setSaveConfirm(true);
            setTimeout(() => setSaveConfirm(false), 3000);
        }
    };

    const handleManualSync = async () => {
        setIsInitialSyncing(true);
        try {
            const configId = editingArr ? editingArr.id : syncConfigId;
            const syncResult = await triggerSync(configId);

            if (syncResult.success) {
                Alert.success('Manual sync complete!');
            } else {
                Alert.error(syncResult.error || 'Failed to start manual sync');
            }
        } catch (error) {
            Alert.error('Failed to start manual sync');
        } finally {
            setIsInitialSyncing(false);
            setShowSyncConfirm(false);
            onSubmit();
        }
    };

    const handleDelete = async () => {
        if (deleteConfirm) {
            try {
                const result = await deleteArrConfig(editingArr.id);
                if (result.success) {
                    Alert.success('Configuration deleted successfully');
                    onSubmit();
                }
            } catch (error) {
                Alert.error('Failed to delete configuration');
            }
            setDeleteConfirm(false);
        } else {
            setDeleteConfirm(true);
            setTimeout(() => setDeleteConfirm(false), 3000);
        }
    };

    const handleInputChange = e => {
        const {id, value} = e.target;
        setFormData(prev => {
            // Handle sync method changes
            if (id === 'sync_method') {
                return {
                    ...prev,
                    [id]: value,
                    data_to_sync:
                        value === 'manual'
                            ? {profiles: [], customFormats: []}
                            : prev.data_to_sync || {
                                  profiles: [],
                                  customFormats: []
                              }
                };
            }

            // Handle other input changes
            return {
                ...prev,
                [id]: id === 'sync_interval' ? parseInt(value) || 0 : value
            };
        });

        if (errors[id]) {
            setErrors(prev => ({...prev, [id]: ''}));
        }
    };

    const handleDataToggle = (type, name) => {
        setFormData(prev => {
            // Ensure data_to_sync exists with proper structure
            const currentData = prev.data_to_sync || {
                profiles: [],
                customFormats: []
            };
            const currentArray = currentData[type] || [];

            return {
                ...prev,
                data_to_sync: {
                    ...currentData,
                    [type]: currentArray.includes(name)
                        ? currentArray.filter(item => item !== name)
                        : [...currentArray, name]
                }
            };
        });

        if (errors.data_to_sync) {
            setErrors(prev => ({...prev, data_to_sync: ''}));
        }
    };

    const handleAddTag = e => {
        e.preventDefault();
        if (tagInput.trim()) {
            if (!formData.tags.includes(tagInput.trim())) {
                setFormData(prev => ({
                    ...prev,
                    tags: [...prev.tags, tagInput.trim()]
                }));
            }
            setTagInput('');
        }
    };

    const handleRemoveTag = tagToRemove => {
        setFormData(prev => ({
            ...prev,
            tags: prev.tags.filter(tag => tag !== tagToRemove)
        }));
    };

    const handleTagInputKeyDown = e => {
        if (e.key === 'Enter' || e.key === ',') {
            e.preventDefault();
            handleAddTag(e);
        }
    };

    return {
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
    };
};
