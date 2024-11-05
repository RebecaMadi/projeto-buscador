import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ProcessDetails from '../ProcessDetails';

describe('ProcessDetails Component', () => {
  const mockProcess = {
    id: '1',
    number: '12345',
    distributionDate: '2024-10-01',
    movements: [{ date: '2024-10-01', description: 'Movimentação 1' }],
    related_people: [{ name: 'João Silva', role: 'Autor' }],
    representedPersonLawyers: [{ name: 'Dr. Maria', representedPerson: 'João Silva' }],
    caseValue: 10000.0,
    court: 'TJAL',
    type: 'Cível',
    nature: 'Ação Ordinária',
    subject: 'Algum assunto',
    judge: 'Dr. Carlos',
  };

  test('Renderiza os detalhes do processo na variante control', () => {
    render(<ProcessDetails process={mockProcess} variant="control" onShowOfferModal={jest.fn()} />);

    expect(screen.getByText(/Processo nº 12345 do TJAL/i)).toBeInTheDocument();
    expect(screen.getByText(/Distribuído em: 01\/10\/2024/i)).toBeInTheDocument();
    expect(screen.getByText(/R\$ 10000.00/i)).toBeInTheDocument();
    expect(screen.getByText(/Dr. Carlos/i)).toBeInTheDocument();
    expect(screen.getByText(/Movimentação 1/i)).toBeInTheDocument();
    expect(screen.getByText(/Algum assunto/i)).toBeInTheDocument();
    const representedPerson = screen.getAllByText(/João Silva/i);
    expect(representedPerson).toHaveLength(2); 
    expect(screen.getByText(/Autor/i)).toBeInTheDocument();
    expect(screen.getByText(/Dr. Maria/i)).toBeInTheDocument();
    expect(screen.getByText(/Tribunal/i)).toBeInTheDocument();
    expect(screen.getByText(/Cível/i)).toBeInTheDocument();
    expect(screen.getByText(/Ação Ordinária/i)).toBeInTheDocument();
  });

  test('Exibe o modal de oferta na variante variant-a', () => {
    render(<ProcessDetails process={mockProcess} variant="variant-a" onShowOfferModal={jest.fn()} />);

    expect(screen.getByRole('button', { name: /Ver Oferta/i })).toBeInTheDocument();
  });

  test('Não exibe o modal de oferta na variante control', () => {
    render(<ProcessDetails process={mockProcess} variant="control" onShowOfferModal={jest.fn()} />);

    expect(screen.queryByRole('button', { name: /Ver Oferta/i })).not.toBeInTheDocument();
  });

  test('Chama o modal de oferta se o botão de ver oferta for clicado (variant-a)', () => {
    const mockShowOfferModal = jest.fn();
    render(<ProcessDetails process={mockProcess} variant="variant-a" onShowOfferModal={mockShowOfferModal} />);

    const button = screen.getByRole('button', { name: /Ver Oferta/i });
    fireEvent.click(button);

    expect(mockShowOfferModal).toHaveBeenCalledTimes(1);
  });
});
