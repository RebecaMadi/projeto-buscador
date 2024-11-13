import { gql, useLazyQuery, useQuery } from "@apollo/client";
import { useState, FC, useEffect } from "react";
import SearchBar from "../components/SearchBar";
import ResultList from "../components/ResultList";
import ProcessDetails from "../components/ProcessDetails";
import { OfferModal } from "../components/OfferModal";
import styles from '../styles/Home.module.css';

//Query para pegar a SERP do backend.
const SEARCH_PROCESSES_QUERY = gql`
  query SearchProcesses($query: String!, $court: String) {
    search(query: $query, court: $court) {
      id
      number
      court
      distributionDate
      movements {
        date
        description
      }
      related_people {
        name
        role
      }
      representedPersonLawyers {
        name
        representedPerson
      }
      caseValue
      type
      nature
      subject
      judge
    }
  }
`;

//Query para pegar um documento com id específico do backend.
const GET_PROCESS_DETAILS_QUERY = gql`
  query GetProcessDetails($id: String!) {
    searchbyid(id: $id) {
      id
      number
      court
      distributionDate
      movements {
        date
        description
      }
      related_people {
        name
        role
      }
      representedPersonLawyers {
        name
        representedPerson
      }
      caseValue
      type
      nature
      subject
      judge
      instance
    }
  }
`;

//Query para sortear uma variante de experimento.
const SORTED_EXP_QUERY = gql`
  query GetExperimentVariant($alternative: String) {
    experimentData(alternative: $alternative) { 
      status
      experiment_group {
        name
      }
      experiment {
        name
      }
      alternative {
        name
      }
      client_id
      participating
      simulating
    }
  }
`;

const Home: FC = () => {

  const [results, setResults] = useState<any[]>([]);
  const [selectedProcess, setSelectedProcess] = useState<any | null>(null);
  const [showOfferModal, setShowOfferModal] = useState(false);
  const [variant, setVariant] = useState<string | null>("control");
  const [alternative, setAlternative] = useState<string | null>("control"); 
  const [participating, setParticipating] = useState<boolean>(false); 
  const [resultBool, setResultBool] = useState<Boolean>(false);
  const [simulating] = useState<boolean>(false); 

  const { loading: loadingVariant} = useQuery(SORTED_EXP_QUERY, {
    variables: { alternative }, 
    onCompleted: (data) => {
      if (data.experimentData?.alternative) {
        const variantName = data.experimentData.alternative.name;
        setVariant(variantName);
      }
    },
    onError: (error) => {
      console.error("Erro ao buscar variante do experimento:",error);
    },
  });
  console.log("Usuário está participando do experimento? ->", participating);
  console.log("Nova requisição de experimento? -> ", loadingVariant);

  const [searchProcesses] = useLazyQuery(SEARCH_PROCESSES_QUERY, {
    onCompleted: (data) => {
      setResults(data.search);
      setSelectedProcess(null);
    },
    onError: (error) => {
      console.error("Erro ao buscar processos:", error);
    },
  });

  const [getProcessDetails] = useLazyQuery(GET_PROCESS_DETAILS_QUERY, {
    onCompleted: (data) => {
      console.log("Detalhes do processo recebidos:", data.searchbyid);
      setSelectedProcess(data.searchbyid); 
    },
    onError: (error) => {
      console.error("Erro ao buscar detalhes do processo:", error);
    },
  });

  const handleSearch = (query: string, court: string) => {
    setResultBool(true);
    searchProcesses({ variables: { query, court } });
  };

  const handleSelectProcess = (id: string) => {
    setParticipating(variant === "variant-a");
    getProcessDetails({ variables: { id } });
  };

  useEffect(() => {
    console.log("Participating mudou: ", participating);
  }, [participating]);

  const handleShowOfferModal = () => {
    setShowOfferModal(true);
  };

  const handleCloseOfferModal = () => {
    setShowOfferModal(false);
  };

  const updateQueryParameters = (newAlternative: string) => {
    setAlternative(newAlternative);
  };

  const handleVariantExit = () => {
    setVariant("control"); 
    handleCloseOfferModal();
  };

  useEffect(() => {
    console.log("Variant: ", variant);
  }, [alternative]);

  return (
    <div className={styles.container}>
      <h1>Buscador de Processos</h1>
      {simulating && (
        <div className={styles.queryParameters}>
          <input 
            className={styles.input} 
            type="text" 
            placeholder="Alternative"
            value={alternative || ""}
            onChange={(e) => updateQueryParameters(e.target.value)}
          />
          <button className={styles.button} onClick={() => updateQueryParameters(alternative || "")}>
            Testar variantes
          </button>
        </div>
      )}
      <SearchBar onSearch={handleSearch} />
      {!selectedProcess &&  resultBool && <ResultList results={results} onSelect={handleSelectProcess} />}
      {selectedProcess && (
        <ProcessDetails
          process={selectedProcess}
          variant={variant || "control"} 
          onShowOfferModal={handleShowOfferModal}
        />
      )}
      {showOfferModal && 
        selectedProcess && (
          <OfferModal 
            onClose={handleCloseOfferModal} 
            lawsuitNumber={selectedProcess.number} 
            movementId={String(selectedProcess.movements.length - 1)} 
            onVariantExit={handleVariantExit} 
          />
        )}
    </div>
  );
};

export default Home;
