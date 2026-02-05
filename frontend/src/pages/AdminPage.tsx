
import React, { useEffect, useState } from 'react';
import {
    getUsers,
    updateUserRole,
    getUsersWithActivity,
    getUserSessions,
    getSessionEvents,
    type User,
    type UserWithActivity,
    type Session,
    type SessionEvent
} from '../api';
import { useSettings } from '../contexts/SettingsContext';
import SessionDetailModal from '../components/SessionDetailModal';
import './AdminPage.css';

const AdminPage: React.FC = () => {
    const { formatDateTime, formatDate } = useSettings();
    const [users, setUsers] = useState<User[]>([]);
    const [usersWithActivity, setUsersWithActivity] = useState<UserWithActivity[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [expandedUser, setExpandedUser] = useState<string | null>(null);
    const [userSessions, setUserSessions] = useState<Session[]>([]);
    const [sessionsLoading, setSessionsLoading] = useState(false);
    const [selectedSession, setSelectedSession] = useState<string | null>(null);
    const [sessionEvents, setSessionEvents] = useState<SessionEvent[]>([]);
    const [eventsLoading, setEventsLoading] = useState(false);
    const [activeTab, setActiveTab] = useState<'users' | 'activity'>('users');

    const fetchUsers = async () => {
        try {
            const [userData, activityData] = await Promise.all([
                getUsers(),
                getUsersWithActivity().catch((e) => {
                    console.error('getUsersWithActivity failed:', e);
                    return [];
                })
            ]);
            console.log('Activity data received:', activityData);
            setUsers(userData);
            setUsersWithActivity(activityData);
            setError(null);
        } catch (err) {
            setError('Failed to fetch users');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUsers();
    }, []);

    const handleRoleChange = async (uid: string, newRole: string) => {
        try {
            await updateUserRole(uid, newRole);
            setUsers(users.map(u => u.uid === uid ? { ...u, role: newRole as 'pending' | 'user' | 'admin' } : u));
        } catch (err) {
            console.error('Failed to update status', err);
            alert('Failed to update status');
        }
    };

    const handleUserClick = async (uid: string) => {
        if (expandedUser === uid) {
            setExpandedUser(null);
            setUserSessions([]);
            return;
        }

        setExpandedUser(uid);
        setSessionsLoading(true);
        try {
            const sessions = await getUserSessions(uid);
            setUserSessions(sessions);
        } catch (err) {
            console.error('Failed to fetch sessions', err);
            setUserSessions([]);
        } finally {
            setSessionsLoading(false);
        }
    };

    const handleSessionClick = async (sessionId: string) => {
        setSelectedSession(sessionId);
        setEventsLoading(true);
        try {
            const events = await getSessionEvents(sessionId);
            setSessionEvents(events);
        } catch (err) {
            console.error('Failed to fetch events', err);
            setSessionEvents([]);
        } finally {
            setEventsLoading(false);
        }
    };

    const getActivityForUser = (uid: string): UserWithActivity | undefined => {
        return usersWithActivity.find(u => u.uid === uid);
    };

    if (loading) return (
        <div className="admin-container">
            <div className="container" style={{ paddingTop: '4rem', textAlign: 'center' }}>Loading...</div>
        </div>
    );

    return (
        <div className="admin-container">
            <div className="container" style={{ paddingTop: '2rem' }}>
                <div className="admin-header">
                    <h1 className="admin-title">User Administration</h1>
                    <div className="tab-buttons">
                        <button
                            className={`tab-btn ${activeTab === 'users' ? 'active' : ''}`}
                            onClick={() => setActiveTab('users')}
                        >
                            👥 User Management
                        </button>
                        <button
                            className={`tab-btn ${activeTab === 'activity' ? 'active' : ''}`}
                            onClick={() => setActiveTab('activity')}
                        >
                            📊 Activity Log
                        </button>
                    </div>
                </div>

                {error && <div className="error-message">{error}</div>}

                {activeTab === 'users' && (
                    <div className="table-container">
                        <table className="admin-table">
                            <thead>
                                <tr>
                                    <th>Email</th>
                                    <th>Role</th>
                                    <th>Last Login</th>
                                    <th>Created</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {users.map((user) => (
                                    <tr key={user.uid}>
                                        <td>{user.email}</td>
                                        <td>
                                            <span className={`role-badge ${user.role}`}>
                                                {user.role}
                                            </span>
                                        </td>
                                        <td>
                                            {formatDateTime(user.last_login)}
                                        </td>
                                        <td>
                                            {formatDate(user.created_at)}
                                        </td>
                                        <td>
                                            <div className="action-buttons">
                                                {user.role !== 'admin' && (
                                                    <>
                                                        <button
                                                            onClick={() => handleRoleChange(user.uid, 'user')}
                                                            className="btn-action btn-approve"
                                                            disabled={user.role === 'user'}
                                                        >
                                                            Approve
                                                        </button>
                                                        <button
                                                            onClick={() => handleRoleChange(user.uid, 'pending')}
                                                            className="btn-action btn-suspend"
                                                            disabled={user.role === 'pending'}
                                                        >
                                                            Suspend
                                                        </button>
                                                        <button
                                                            onClick={() => handleRoleChange(user.uid, 'admin')}
                                                            className="btn-action btn-admin"
                                                        >
                                                            Make Admin
                                                        </button>
                                                    </>
                                                )}
                                                {user.role === 'admin' && (
                                                    <span className="role-badge admin">Admin</span>
                                                )}
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                {activeTab === 'activity' && (
                    <div className="table-container">
                        <table className="admin-table activity-table">
                            <thead>
                                <tr>
                                    <th>User</th>
                                    <th>Event Time</th>
                                    <th>Event Type</th>
                                    <th>Details</th>
                                </tr>
                            </thead>
                            <tbody>
                                {users.map((user) => {
                                    const activity = getActivityForUser(user.uid);
                                    const isExpanded = expandedUser === user.uid;

                                    return (
                                        <React.Fragment key={user.uid}>
                                            {/* User summary row */}
                                            <tr
                                                className="user-row clickable"
                                                onClick={() => handleUserClick(user.uid)}
                                            >
                                                <td>
                                                    <span className="user-email">{user.email}</span>
                                                    <span className={`role-badge ${user.role}`}>{user.role}</span>
                                                </td>
                                                <td className="stat-cell">
                                                    {formatDateTime(activity?.last_activity)}
                                                </td>
                                                <td className="stat-cell">
                                                    <span className="stat-inline">📊 {activity?.total_sessions || 0} sessions</span>
                                                    <span className="stat-inline">📝 {activity?.total_events || 0} events</span>
                                                    {(activity?.total_errors || 0) > 0 && (
                                                        <span className="stat-inline error-stat">❌ {activity?.total_errors} errors</span>
                                                    )}
                                                </td>
                                                <td>
                                                    <span className="expand-icon">{isExpanded ? '▼' : '▶'}</span>
                                                </td>
                                            </tr>

                                            {/* Expanded session rows */}
                                            {isExpanded && (
                                                sessionsLoading ? (
                                                    <tr className="session-row">
                                                        <td colSpan={4} className="loading-cell">Loading sessions...</td>
                                                    </tr>
                                                ) : userSessions.length === 0 ? (
                                                    <tr className="session-row">
                                                        <td colSpan={4} className="empty-cell">No sessions recorded</td>
                                                    </tr>
                                                ) : (
                                                    userSessions.map((session) => (
                                                        <tr
                                                            key={session.session_id}
                                                            className={`session-row clickable ${session.error_count > 0 ? 'has-errors' : ''}`}
                                                            onClick={() => handleSessionClick(session.session_id)}
                                                        >
                                                            <td className="indent-cell">↳ Session</td>
                                                            <td>{formatDateTime(session.started_at)}</td>
                                                            <td>
                                                                <span className="stat-inline">📝 {session.event_count} events</span>
                                                                {session.error_count > 0 && (
                                                                    <span className="stat-inline error-stat">❌ {session.error_count} errors</span>
                                                                )}
                                                            </td>
                                                            <td>
                                                                <button className="btn-view">View</button>
                                                            </td>
                                                        </tr>
                                                    ))
                                                )
                                            )}
                                        </React.Fragment>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            {selectedSession && !eventsLoading && (
                <SessionDetailModal
                    events={sessionEvents}
                    sessionId={selectedSession}
                    onClose={() => {
                        setSelectedSession(null);
                        setSessionEvents([]);
                    }}
                />
            )}

            {eventsLoading && (
                <div className="loading-overlay">
                    <div className="loading-spinner">Loading events...</div>
                </div>
            )}
        </div>
    );
};

export default AdminPage;
