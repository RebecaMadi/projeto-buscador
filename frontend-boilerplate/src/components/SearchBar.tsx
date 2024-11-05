import { useState, FC } from 'react';
import styles from '../styles/SearchBar.module.css';
import Filter from './Filter';

interface SearchBarProps {
  onSearch: (query: string, filter: string) => void; 
}

const SearchBar: FC<SearchBarProps> = ({ onSearch }) => {
  const [query, setQuery] = useState<string>('');
  const [selectedFilter, setSelectedFilter] = useState<string>('');

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSearch(query, selectedFilter); 
  };

  return (
    <form className={styles.searchBar} onSubmit={handleSearch}>
      <input
        type="text"
        placeholder="Digite um número de processo..."
        value={query}
        onChange={(e) => setQuery(e.target.value)} 
        className={styles.input}
      />
      <Filter selectedFilter={selectedFilter} onFilterChange={setSelectedFilter} /> {}
      <button type="submit" className={styles.button}>Buscar</button>
    </form>
  );
};

export default SearchBar;
