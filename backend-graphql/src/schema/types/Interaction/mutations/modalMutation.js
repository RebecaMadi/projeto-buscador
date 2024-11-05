import { GraphQLString } from 'graphql';
import { InteractionType } from '../typeDefs';

export const mutationResponse = {
  type: InteractionType,
  args: {
    lawsuitNumber: { type: GraphQLString },
    movementId: { type: GraphQLString },
  },
  resolve: async (_, { lawsuitNumber, movementId }) => {
    try {
      console.log(lawsuitNumber, movementId);

      const currentData = new Date().toISOString(); 
      console.log("mutation\n");
      return {
        status: true,
        message: "Modificação salva!",
        movement: {
          lastInteraction: currentData, 
        },
      };
    } catch (error) {
      console.error("Erro ao buscar dados da experiência:", error);
      throw new Error("Não foi possível realizar a busca.");
    }
  },
};
