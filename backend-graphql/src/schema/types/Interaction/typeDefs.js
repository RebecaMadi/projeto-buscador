import { GraphQLObjectType, GraphQLString, GraphQLBoolean } from 'graphql';

const MovementType = new GraphQLObjectType({
  name: 'MovementType',
  fields: () => ({
    lastInteraction: { type: GraphQLString },
  }),
});

export const InteractionType = new GraphQLObjectType({
  name: 'InteractionType',
  fields: () => ({
    status: { type: GraphQLBoolean }, 
    message: { type: GraphQLString }, 
    movement: { type: MovementType }, 
  }),
});
