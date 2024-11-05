import { GraphQLSchema, GraphQLObjectType } from 'graphql';
import { searchQuery,  searchQueryId} from './types/Process/queries';
import { sortedExp } from './types/Experiment/queries';
import { getModal } from './types/Modal/queries';
import { mutationResponse } from './types/Interaction/mutations';

const QueryType = new GraphQLObjectType({
  name: 'Query',
  fields: () => ({
    search: searchQuery,
    searchbyid: searchQueryId,
    experimentData: sortedExp,
    nextPlanModal: getModal,
  }),
});

const MutationType = new GraphQLObjectType({
  name: 'Mutation',
  fields: () => ({
    RegisterLastInteraction: mutationResponse,
  }),
});

const schema = new GraphQLSchema({
  query: QueryType,
  mutation: MutationType,
});

export default schema;
