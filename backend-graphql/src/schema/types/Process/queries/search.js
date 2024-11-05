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
      let params = {};
      params.query = query;
      if (court) {
        params.court = court;
      }
      const response = await axios.get('http://localhost:9777/search-serp', {
        params, 
      });
      console.log(response.data)
      return response.data; 
    } catch (error) {
      console.error("Erro ao buscar processos com a query:", query, error);
      throw new Error("Não foi possível realizar a busca.");
    }
  }
}