import { GraphQLObjectType, GraphQLString, GraphQLList, GraphQLID, GraphQLFloat } from 'graphql';

const MovementType = new GraphQLObjectType({
  name: 'Activity',
  fields: () => ({
    date: { type: GraphQLString },
    description: { type: GraphQLString },
  }),
});

const PartyType = new GraphQLObjectType({
  name: 'RelatedPerson',
  fields: () => ({
    name: { type: GraphQLString },
    role: { type: GraphQLString },
  }),
});

const LawyerType = new GraphQLObjectType({
  name: 'RepresentedPersonLawyer',
  fields: () => ({
    name: { type: GraphQLString },
    representedPerson: { type: GraphQLString },
  }),
});

export const ProcessType = new GraphQLObjectType({
  name: 'Lawsuit',
  fields: () => ({
    id: { type: GraphQLID },
    number: { type: GraphQLString },
    distributionDate: { type: GraphQLString },
    movements: { type: new GraphQLList(MovementType) },
    related_people: { type: new GraphQLList(PartyType) },
    representedPersonLawyers: { type: new GraphQLList(LawyerType) },
    caseValue: { type: GraphQLFloat },
    court: { type: GraphQLString },
    instance: { type: GraphQLString },
    type: { type: GraphQLString },
    nature: { type: GraphQLString },
    subject: { type: GraphQLString },
    judge: { type: GraphQLString },
  }),
});
