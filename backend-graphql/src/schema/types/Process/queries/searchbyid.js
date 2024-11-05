import { GraphQLObjectType, GraphQLNonNull, GraphQLString } from 'graphql';
import { ProcessType } from '../typeDefs';
const axios = require('axios');

export const searchQueryId = {
  type: ProcessType, 
  args: {
    id: { type: new GraphQLNonNull(GraphQLString) }, 
  },
  resolve: async (_, { id }) => {
    try {
      console.log("???");
      const response = await axios.get(`http://localhost:9777/search-serp/${id}`); 
      return response.data; 
    } catch (error) {
      console.error("Erro ao buscar o processo com o ID:", id, error);
      throw new Error("Não foi possível realizar a busca pelo ID.");
    }
  }
};
