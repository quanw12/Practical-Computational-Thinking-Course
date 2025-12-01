import React, { useState } from 'react';

interface SearchPanelProps {
  onSearch: (destination: string) => void;
  loading: boolean;
  error: string | null;
}

const SearchPanel: React.FC<SearchPanelProps> = ({ onSearch, loading, error }) => {
  const [destination, setDestination] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (destination.trim()) {
      onSearch(destination.trim());
    }
  };

  return (
    <div className="search-panel">
      <form onSubmit={handleSubmit} className="search-container">
        <input
          type="text"
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
          placeholder="Enter a Vietnamese destination (e.g., Da Nang, Hue, Nha Trang, Can Tho)"
          className="destination-input"
          disabled={loading}
        />
        <button 
          type="submit" 
          className="search-btn"
          disabled={loading || !destination.trim()}
        >
          {loading ? 'Exploring...' : 'Explore'}
        </button>
      </form>
      
      {loading && <div className="loading">Discovering amazing attractions...</div>}
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default SearchPanel;