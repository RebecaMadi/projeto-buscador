import { GraphQLObjectType, GraphQLString, GraphQLList } from 'graphql';

const HeaderType = new GraphQLObjectType({
  name: 'Header',
  fields: () => ({
    title: { type: GraphQLString },
    subtitle: { type: GraphQLString },
  }),
});

const PriceType = new GraphQLObjectType({
  name: 'Price',
  fields: () => ({
    current: { type: GraphQLString },
    next: { type: GraphQLString },
    period: { type: GraphQLString },
  }),
});

const ButtonType = new GraphQLObjectType({
  name: 'Button',
  fields: () => ({
    label: { type: GraphQLString },
  }),
});

const FooterType = new GraphQLObjectType({
  name: 'Footer',
  fields: () => ({
    text: { type: GraphQLString },
  }),
});

const BodyType = new GraphQLObjectType({
  name: 'Body',
  fields: () => ({
    benefits: { type: new GraphQLList(GraphQLString) },
    price: { type: PriceType }, 
    button: { type: ButtonType }, 
  }),
});

export const ModalType = new GraphQLObjectType({
  name: 'ModalType',
  fields: () => ({
    header: { type: HeaderType }, 
    body: { type: BodyType }, 
    footer: { type: FooterType }, 
  }),
});
