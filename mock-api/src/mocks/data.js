export const processes = [
  {
    id: "1235",
    number: "0001234-56.2023.8.19.0001",
    court: "TJAL",
    nature: "Cível",
    type: "Ação de Indenização",
    subject: "Danificação de imagem",
    distributionDate: "2023-01-15",
    judge: "Dr. João da Silva",
    caseValue: 100000.00,
    related_people: [
      {
        name: "Pablo Vegetti",
        role: "Autor"
      },
      {
        name: "Clube de Regatas Vasco da Gama",
        role: "Réu"
      }
    ],
    representedPersonLawyers: [
      {
        name: "Dr. Carlos Almeida",
        representedPerson: "Pablo Vegetti"
      },
      {
        name: "Dra. Ana Pereira",
        representedPerson: "Clube de Regatas Vasco da Gama"
      }
    ],
    movements: [
      {
        date: "2023-02-10",
        description: "Distribuição da ação. O processo foi iniciado e distribuído na vara competente, com a designação do juiz Dr. João da Silva para presidir o caso. As partes foram notificadas quanto ao início da ação, tendo sido registrado no sistema de acompanhamento processual."
      },
      {
        date: "2023-03-05",
        description: "Audiência de conciliação. As partes compareceram para uma tentativa de acordo visando a resolução amigável do litígio. Durante a audiência, foram apresentados argumentos e propostas, mas não houve consenso. A audiência foi encerrada, e o processo seguirá para instrução probatória."
      },
      {
        date: "2023-04-12",
        description: "Petição intermediária apresentada pelo réu. A defesa do Clube de Regatas Vasco da Gama protocolou uma petição detalhando argumentos de defesa e apresentando documentos que alegam comprovar a inexistência de dano. Essa petição será analisada pelo juiz, que decidirá sobre a necessidade de provas adicionais."
      },
      {
        date: "2023-06-20",
        description: "Decisão interlocutória. O juiz decidiu pela produção de provas documentais, concedendo prazo de 15 dias para que ambas as partes apresentem qualquer documentação adicional relevante. Essa decisão foi baseada na complexidade dos fatos e na necessidade de análise detalhada para assegurar a justa resolução do caso."
      }
    ]
  }
  ,
  {
    id: "12345",
    number: "0001234-56.2023.6.19.0001",
    court: "TJCE",
    nature: "Cível",
    type: "Ação de Indenização",
    subject: "Danificação de imagem",
    distributionDate: "2023-01-15",
    judge: "Dr. João da Silva",
    caseValue: 100000.00,
    related_people: [
      {
        name: "Pablo Vegetti",
        role: "Autor"
      },
      {
        name: "Clube de Regatas Vasco da Gama",
        role: "Réu"
      }
    ],
    representedPersonLawyers: [
      {
        name: "Dr. Carlos Almeida",
        representedPerson: "Pablo Vegetti"
      },
      {
        name: "Dra. Ana Pereira",
        representedPerson: "Clube de Regatas Vasco da Gama"
      }
    ],
    movements: [
      {
        date: "2023-02-10",
        description: "Distribuição da ação"
      },
      {
        date: "2023-03-05",
        description: "Audiência de conciliação"
      },
      {
        date: "2023-04-12",
        description: "Petição intermediária apresentada pelo réu. A defesa do Clube de Regatas Vasco da Gama protocolou uma petição detalhando argumentos de defesa e apresentando documentos que alegam comprovar a inexistência de dano. Essa petição será analisada pelo juiz, que decidirá sobre a necessidade de provas adicionais."
      },
      {
        date: "2023-06-20",
        description: "Decisão interlocutória. O juiz decidiu pela produção de provas documentais, concedendo prazo de 15 dias para que ambas as partes apresentem qualquer documentação adicional relevante. Essa decisão foi baseada na complexidade dos fatos e na necessidade de análise detalhada para assegurar a justa resolução do caso."
      }
    ]
  }
  ];
  

  export const searchProcesses = (query, court) => {
    console.log("q: ", query)
    return processes.filter(process => {
      const matchesQuery = process.number.toLowerCase().includes(query.toLowerCase());
  
      if (!court) {
        return matchesQuery;
      }
  
      return matchesQuery && process.court === court;
    });
  };
  
  