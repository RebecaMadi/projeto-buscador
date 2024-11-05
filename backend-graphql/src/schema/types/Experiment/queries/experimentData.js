import { GraphQLString } from 'graphql';
import  {ResponseType}  from '../typeDefs';
const axios = require('axios');

export const sortedExp = {
  type: ResponseType,
  args: {
    alternative: { type: GraphQLString },
    simulating: { type: GraphQLString },
  },
  resolve: async (_, {alternative, simulating}) => {
    try {
      let params = {};
      if(alternative){
        params.alternative = alternative;
      }
      if (simulating) {
        params.simulating = simulating;
      }
      const response = await axios.get('http://localhost:9777/experiment/participate', {
        params, 
      });
      console.log('Resposta da API:', response.data);
      return response.data; 
    } catch (error) {
      console.error("Erro ao buscar dados da experiência:", error);
      throw new Error("Não foi possível realizar a busca.");
    }
  }
}