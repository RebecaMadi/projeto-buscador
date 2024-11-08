import { GraphQLList, GraphQLString, GraphQLNonNull } from 'graphql';
import { ProcessType } from '../typeDefs';
const axios = require('axios');

export const searchQuery = {
  type: new GraphQLList(ProcessType),
  args: {
    query: { type: new GraphQLNonNull(GraphQLString) },
    court: { type: GraphQLString },
  },
  resolve: async (_, { query, court }) => {
    try {
      const requestBody = {
        query: query,
        filters: {},
      };

      if (court) {
        requestBody.filters.court = court;
      }

      const response = await axios.post('http://localhost:3003/search', requestBody, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      console.log(response.data)
      return response.data; 
    } catch (error) {
      console.error("Erro ao buscar processos com a query:", query, error);
      throw new Error("Não foi possível realizar a busca. ", error);
    }
  }
}