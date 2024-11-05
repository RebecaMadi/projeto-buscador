import { FC } from "react";

interface ResultItemProps {
  id: string;
  title: string;
  onSelect: (id: string) => void; 
}

const ResultItem: FC<ResultItemProps> = ({ id, title, onSelect }) => {
  return (
    <div onClick={() => onSelect(id)}  className="result-item" >
      <h3>{title}</h3>
    </div>
  );
};

export default ResultItem;
