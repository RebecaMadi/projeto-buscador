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
      const requestBody = {
        id: id,
      };
      const response = await axios.post('http://localhost:3003/searchbyid', {"id": id}, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      return response.data; 
    } catch (error) {
      console.error("Erro ao buscar o processo com o ID:", id, error);
      throw new Error("Não foi possível realizar a busca pelo ID.");
    }
  }
};
