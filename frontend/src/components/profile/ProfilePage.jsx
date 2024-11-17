import React, {useState, useEffect} from 'react';
import {useNavigate} from 'react-router-dom';
import ProfileCard from './ProfileCard';
import ProfileModal from './ProfileModal';
import AddNewCard from '../ui/AddNewCard';
import {getProfiles, getFormats, getGitStatus} from '../../api/api';
import FilterMenu from '../ui/FilterMenu';
import SortMenu from '../ui/SortMenu';
import {Loader} from 'lucide-react';

function ProfilePage() {
    const [profiles, setProfiles] = useState([]);
    const [formats, setFormats] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedProfile, setSelectedProfile] = useState(null);
    const [sortBy, setSortBy] = useState('title');
    const [filterType, setFilterType] = useState('none');
    const [filterValue, setFilterValue] = useState('');
    const [allTags, setAllTags] = useState([]);
    const [isCloning, setIsCloning] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [mergeConflicts, setMergeConflicts] = useState([]);

    const navigate = useNavigate();

    const loadingMessages = [
        'Profiling your media collection...',
        'Organizing your digital hoard...',
        'Calibrating the flux capacitor...',
        'Synchronizing with the movie matrix...',
        'Optimizing your binge-watching potential...'
    ];

    useEffect(() => {
        fetchGitStatus();
    }, []);

    const fetchProfiles = async () => {
        try {
            const fetchedProfiles = await getProfiles();
            setProfiles(fetchedProfiles);
            const tags = [
                ...new Set(
                    fetchedProfiles.flatMap(profile => profile.tags || [])
                )
            ];
            setAllTags(tags);
        } catch (error) {
            console.error('Error fetching profiles:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const fetchFormats = async () => {
        try {
            const fetchedFormats = await getFormats();
            setFormats(fetchedFormats);
        } catch (error) {
            console.error('Error fetching formats:', error);
        }
    };

    const fetchGitStatus = async () => {
        try {
            const result = await getGitStatus();
            if (result.success) {
                setMergeConflicts(result.data.merge_conflicts || []);
                if (result.data.merge_conflicts.length === 0) {
                    fetchProfiles();
                    fetchFormats();
                } else {
                    setIsLoading(false);
                }
            }
        } catch (error) {
            console.error('Error fetching Git status:', error);
            setIsLoading(false);
        }
    };

    const handleOpenModal = (profile = null) => {
        const safeProfile = profile
            ? {
                  ...profile,
                  custom_formats: profile.custom_formats || []
              }
            : null;
        setSelectedProfile(safeProfile);
        setIsModalOpen(true);
        setIsCloning(false);
    };

    const handleCloseModal = () => {
        setSelectedProfile(null);
        setIsModalOpen(false);
        setIsCloning(false);
    };

    const handleCloneProfile = profile => {
        const clonedProfile = {
            ...profile,
            id: 0,
            name: `${profile.name} [COPY]`,
            custom_formats: profile.custom_formats || []
        };
        setSelectedProfile(clonedProfile);
        setIsModalOpen(true);
        setIsCloning(true);
    };

    const handleSaveProfile = () => {
        fetchProfiles();
        handleCloseModal();
    };

    const formatDate = dateString => {
        return new Date(dateString).toLocaleString();
    };

    const sortedAndFilteredProfiles = profiles
        .filter(profile => {
            if (filterType === 'tag') {
                return profile.tags && profile.tags.includes(filterValue);
            }
            if (filterType === 'date') {
                const profileDate = new Date(profile.date_modified);
                const filterDate = new Date(filterValue);
                return profileDate.toDateString() === filterDate.toDateString();
            }
            return true;
        })
        .sort((a, b) => {
            if (sortBy === 'name') return a.name.localeCompare(b.name);
            if (sortBy === 'dateCreated')
                return new Date(b.date_created) - new Date(a.date_created);
            if (sortBy === 'dateModified')
                return new Date(b.date_modified) - new Date(a.date_modified);
            return 0;
        });

    const hasConflicts = mergeConflicts.length > 0;

    if (isLoading) {
        return (
            <div className='flex flex-col items-center justify-center h-screen'>
                <Loader size={48} className='animate-spin text-blue-500 mb-4' />
                <p className='text-lg font-medium text-gray-700 dark:text-gray-300'>
                    {
                        loadingMessages[
                            Math.floor(Math.random() * loadingMessages.length)
                        ]
                    }
                </p>
            </div>
        );
    }

    if (hasConflicts) {
        return (
            <div className='bg-gray-900 text-white'>
                <div className='mt-8 flex justify-between items-center'>
                    <h4 className='text-xl font-extrabold'>
                        Merge Conflicts Detected
                    </h4>
                    <button
                        onClick={() => navigate('/settings')}
                        className='bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition'>
                        Resolve Conflicts
                    </button>
                </div>

                <div className='mt-6 p-4 bg-gray-800 rounded-lg shadow-md'>
                    <h3 className='text-xl font-semibold'>What Happened?</h3>
                    <p className='mt-2 text-gray-300'>
                        This page is locked because there are unresolved merge
                        conflicts. You need to address these conflicts in the
                        settings page before continuing.
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div>
            <h2 className='text-2xl font-bold mb-4'>Manage Profiles</h2>
            <div className='mb-4 flex items-center space-x-4'>
                <SortMenu sortBy={sortBy} setSortBy={setSortBy} />
                <FilterMenu
                    filterType={filterType}
                    setFilterType={setFilterType}
                    filterValue={filterValue}
                    setFilterValue={setFilterValue}
                    allTags={allTags}
                />
            </div>
            <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-4'>
                {sortedAndFilteredProfiles.map(profile => (
                    <ProfileCard
                        key={profile.id}
                        profile={profile}
                        onEdit={() => handleOpenModal(profile)}
                        onClone={handleCloneProfile}
                        showDate={sortBy !== 'name'}
                        formatDate={formatDate}
                    />
                ))}
                <AddNewCard onAdd={() => handleOpenModal()} />
            </div>
            <ProfileModal
                profile={selectedProfile}
                isOpen={isModalOpen}
                onClose={handleCloseModal}
                onSave={handleSaveProfile}
                formats={formats}
                isCloning={isCloning}
            />
        </div>
    );
}

export default ProfilePage;
