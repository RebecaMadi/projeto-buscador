import  {ModalType}  from '../typeDefs';
const axios = require('axios');

export const getModal = {
  type: ModalType,
  resolve: async (_, { }) => {
    try {
      const response = await axios.get('http://localhost:9777/box-lock');
      console.log('Resposta da API:', response.data);
      return response.data; 
    } catch (error) {
      console.error("Erro ao buscar dados da experiência:", error);
      throw new Error("Não foi possível realizar a busca.");
    }
  }
}