import { FC } from 'react';
import styles from '../styles/Filter.module.css';

interface FilterProps {
  selectedFilter: string;
  onFilterChange: (filter: string) => void;
}

const Filter: FC<FilterProps> = ({ selectedFilter, onFilterChange }) => {
  return (
    <div className={styles.filter}>
      <select 
        value={selectedFilter} 
        onChange={(e) => onFilterChange(e.target.value)} 
        className={styles.select}
      >
        <option value="">Selecione um tribunal</option>
        <option value="TJAL">TJAL</option>
        <option value="TJCE">TJCE</option>
      </select>
    </div>
  );
};

export default Filter;
