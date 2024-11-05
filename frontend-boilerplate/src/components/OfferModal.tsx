import React, { FC, useEffect } from 'react';
import styles from '../styles/OfferModal.module.css';
import { gql, useLazyQuery, useMutation } from "@apollo/client";

interface OfferModalProps {
  onClose: () => void;
  lawsuitNumber: string;
  movementId: string; 
  onVariantExit: () => void; 
}

const SEARCH_MODAL = gql`
  query {
    nextPlanModal {
      header {
        title
        subtitle
      }
      body {
        benefits
        price {
          current
          next
          period
        }
        button {
          label
        }
      }
      footer {
        text
      }
    }
  }
`;

const ACCEPT_OFFER_MUTATION = gql`
  mutation AcceptOffer($lawsuitNumber: String!, $movementId: String!) {
    RegisterLastInteraction(lawsuitNumber: $lawsuitNumber, movementId: $movementId) {
      status
      message
      movement {
        lastInteraction
      }
    }
  }
`;

export const OfferModal: FC<OfferModalProps> = ({ onClose, lawsuitNumber, movementId, onVariantExit }) => {
  const [loadOfferData, { data, loading, error }] = useLazyQuery(SEARCH_MODAL);
  const [acceptOffer, { loading: mutationLoading, error: mutationError }] = useMutation(ACCEPT_OFFER_MUTATION);

  useEffect(() => {
    loadOfferData();
  }, [loadOfferData]);

  if (loading) return <p>Carregando...</p>;
  if (error) return <p>Erro ao carregar a oferta.</p>;

  const offerData = data?.nextPlanModal;

  const handleAcceptOffer = () => {
    console.log("Tentando aceitar a oferta...");
    acceptOffer({
      variables: {
        lawsuitNumber,
        movementId,
      },
    })
      .then(response => {
        console.log("Resposta da mutação:", response.data.RegisterLastInteraction);
        console.log(response.data.RegisterLastInteraction.message);
  
        onVariantExit();
        onClose();       
      })
      .catch(err => {
        console.error("Erro ao aceitar a oferta:", err);
      });
  };
  

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <button onClick={onClose} className={styles.closeButton}>×</button>
        
        <div className={styles.modalHeader}>
          <h2>{offerData?.header.title}</h2>
          <p>{offerData?.header.subtitle}</p>
        </div>
        
        <div className={styles.modalBody}>
          <ul className={styles.benefitsList}>
            {offerData?.body.benefits.map((benefit: string, index: number) => (
              <li key={index}>{benefit}</li>
            ))}
          </ul>
          
          <div className={styles.priceInfo}>
            <strong>{offerData?.body.price.current} no {offerData?.body.price.period}</strong>
            <p>Depois {offerData?.body.price.next}</p>
          </div>
          
          <button 
            className={styles.subscribeButton} 
            onClick={handleAcceptOffer}
            disabled={mutationLoading} 
          >
            {mutationLoading ? 'Processando...' : offerData?.body.button.label}
          </button>
          
          {mutationError && <p>Erro ao aceitar a oferta: {mutationError.message}</p>}
        </div>
        
        <div className={styles.footerText}>
          <p>{offerData?.footer.text}</p>
        </div>
      </div>
    </div>
  );
};
