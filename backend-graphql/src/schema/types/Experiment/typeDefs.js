import { GraphQLObjectType, GraphQLString, GraphQLBoolean } from 'graphql';

const ExperimentGroupType = new GraphQLObjectType({
  name: 'ExperimentGroup',
  fields: () => ({
    name: { type: GraphQLString },
  }),
});

const ExperimentType = new GraphQLObjectType({
  name: 'Experiment',
  fields: () => ({
    name: { type: GraphQLString },
  }),
});

const AlternativeType = new GraphQLObjectType({
  name: 'Alternative',
  fields: () => ({
    name: { type: GraphQLString },
  }),
});

export const ResponseType = new GraphQLObjectType({
  name: 'Response',
  fields: () => ({
    status: { type: GraphQLString },
    experiment_group: { type: ExperimentGroupType },
    experiment: { type: ExperimentType },
    alternative: { type: AlternativeType },
    client_id: { type: GraphQLString },
    participating: { type: GraphQLBoolean },
    simulating: { type: GraphQLBoolean },
  }),
});
