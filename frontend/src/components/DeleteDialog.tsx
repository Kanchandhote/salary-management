import React from 'react';

interface Props {
  isOpen: boolean;
  title: string;
  onConfirm: () => void;
  onCancel: () => void;
  loading?: boolean;
}

const DeleteDialog: React.FC<Props> = ({ isOpen, title, onConfirm, onCancel, loading }) => {
  if (!isOpen) return null;
  return (
    <div className="modal-overlay">
      <div className="modal" style={{ maxWidth: 400 }}>
        <h3>Confirm Delete</h3>
        <p>Are you sure you want to delete <strong>{title}</strong>? This action cannot be undone.</p>
        <div className="modal-actions">
          <button className="btn btn-secondary" onClick={onCancel} disabled={loading}>
            Cancel
          </button>
          <button className="btn btn-danger" onClick={onConfirm} disabled={loading}>
            {loading ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteDialog;
