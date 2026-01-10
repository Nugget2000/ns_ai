
import React, { useEffect, useState } from 'react';
import { LoaderCircle } from 'lucide-react';
import { getUsers, updateUserRole, type User } from '../api';
import './AdminPage.css';

const AdminPage: React.FC = () => {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [processingAction, setProcessingAction] = useState<{ uid: string, role: string } | null>(null);

    const fetchUsers = async () => {
        try {
            const data = await getUsers();
            setUsers(data);
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
        setProcessingAction({ uid, role: newRole });
        try {
            await updateUserRole(uid, newRole);
            setUsers(users.map(u => u.uid === uid ? { ...u, role: newRole as User['role'] } : u));
        } catch (err) {
            console.error('Failed to update status', err);
            alert('Failed to update status');
        } finally {
            setProcessingAction(null);
        }
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
                </div>

                {error && <div className="error-message">{error}</div>}

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
                                        {user.last_login ? new Date(user.last_login).toLocaleString() : '-'}
                                    </td>
                                    <td>
                                        {user.created_at ? new Date(user.created_at).toLocaleDateString() : '-'}
                                    </td>
                                    <td>
                                        <div className="action-buttons">
                                            {user.role !== 'admin' && (
                                                <>
                                                    <button
                                                        onClick={() => handleRoleChange(user.uid, 'user')}
                                                        className="btn-action btn-approve"
                                                        disabled={user.role === 'user' || processingAction?.uid === user.uid}
                                                    >
                                                        {processingAction?.uid === user.uid && processingAction?.role === 'user' ? (
                                                            <LoaderCircle size={14} className="spinner" />
                                                        ) : (
                                                            "Approve"
                                                        )}
                                                    </button>
                                                    <button
                                                        onClick={() => handleRoleChange(user.uid, 'pending')}
                                                        className="btn-action btn-suspend"
                                                        disabled={user.role === 'pending' || processingAction?.uid === user.uid}
                                                    >
                                                        {processingAction?.uid === user.uid && processingAction?.role === 'pending' ? (
                                                            <LoaderCircle size={14} className="spinner" />
                                                        ) : (
                                                            "Suspend"
                                                        )}
                                                    </button>
                                                    <button
                                                        onClick={() => handleRoleChange(user.uid, 'admin')}
                                                        className="btn-action btn-admin"
                                                        disabled={processingAction?.uid === user.uid}
                                                    >
                                                         {processingAction?.uid === user.uid && processingAction?.role === 'admin' ? (
                                                            <LoaderCircle size={14} className="spinner" />
                                                        ) : (
                                                            "Make Admin"
                                                        )}
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
            </div>
        </div>
    );
};

export default AdminPage;
