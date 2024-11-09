import { FC } from "react";
import ResultItem from "./ResultItem";
import styles from '../styles/ResultList.module.css'; 

interface ResultListProps {
  results: {
    id: string; 
    number: string; 
    court: string; 
    description: string; 
  }[];
  onSelect: (id: string) => void;
}

const ResultList: FC<ResultListProps> = ({ results, onSelect }) => {
  console.log(results)
  return (
    <div className={styles.resultList}>
      {results.length === 0 || results[0] === undefined? (
        <p> Não conseguimos encontrar um resultado para a sua pesquisa :(</p>
      ) : (results.map((result) => (
        <div 
          key={result.id} 
          className={styles.resultItem}
          onClick={() => onSelect(result.id)} 
        >
          <ResultItem 
            id={result.id} 
            title={`Processo n ${result.number} do ${result.court}`} 
            onSelect={onSelect} 
          />
        </div>
      )))}
    </div>
  );
};

export default ResultList;
