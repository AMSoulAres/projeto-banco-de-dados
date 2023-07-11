import axios from "axios";
import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import AsyncSelect from 'react-select/async';

const serverUrl = "http://localhost:8000/";
export default function EditarTurmaComponent() {
  const { state } = useLocation();
  const [idProfessor, setIdProfessor] = useState(state.idProfessor);
  const [idDisciplina, setIdDisciplina] = useState(state.idDisciplina);
  const [professores, setProfessores] = useState([]);
  const [disciplinas, setDisciplinas] = useState([]);
  const [cadastroError, setCadastroError] = useState('');
  const [cadastroSucesso, setCadastroSucesso] = useState('');

  useEffect(() => {
    const loadData = async () => {
      const responseProfessores = await axios.get(`${serverUrl}read-only/professores`)
      setProfessores(responseProfessores.data)
      const responseDisciplinas = await axios.get(`${serverUrl}read-only/disciplinas`)
      setDisciplinas(responseDisciplinas.data)
    };
    loadData();
  }, [])


  const professorDepartamento = professores.map(item => {
    return {
      label: `${item.nomeProfessor} - ${item.nomeDepartamento}`,
      value: `${item.nomeProfessor}`,
      id: item.idProfessor
    }
  });
  const filterProfessor = (inputValue) => {
    return professorDepartamento
      .filter((i) => {
        return i.value.toLowerCase().includes(inputValue.toLowerCase())
      }
      );
  };

  const loadOptionsProfessor = (
    inputValue,
    callback
  ) => {
    setTimeout(() => {
      callback(filterProfessor(inputValue));
    }, 1000);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(idDisciplina)
    console.log(idProfessor)
    try {
      const response = await axios.put(`${serverUrl}turma/atualiza-turma/${state.id}`, {
        idProfessor: idProfessor,
        idDisciplina: idDisciplina,
      });

      if (response.status === 200) {
        // A conta foi criada com sucesso
        setCadastroSucesso('Turma atualizada com sucesso!');

        // Redirecionar para outra página, se necessário
      } else {
        // Algo deu errado ao criar a conta
        setCadastroError('Não foi possível atualizar a turma. Por favor, tente novamente.');
      }
    } catch (err) {
      if (err.response) {
        if (err.response.status === 400) {
          // Erro de validação (422)
          console.log(err.response)
          setCadastroError(err.response.data.detail);
        }
      } else {
        // Outro erro de requisição
        setCadastroError('Ocorreu um erro ao criar a conta. Por favor, tente novamente.');
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#1a0409]">
      <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-[#f5f7f7]">
            Atualize a turma!
          </h2>
        </div>
        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div className="items-center justify-between">
              <div className="mt-2">
                <label htmlFor="curso" className="block text-sm font-medium leading-6 text-[#f5f7f7]">
                  Professor
                </label>
                <AsyncSelect defaultValue={{
                  label: state.professor,
                  value: state.idProfessor
                }}
                  onChange={(choice) => { setIdProfessor(choice.id) }}
                  cacheOptions loadOptions={loadOptionsProfessor}
                  defaultOptions={professorDepartamento} />
              </div>
              <div className="mt-2">
                <label htmlFor="curso" className="block text-sm font-medium leading-6 text-[#f5f7f7]">
                  Disciplina
                </label>
                <AsyncSelect defaultValue={{
                  label: state.disciplina,
                  value: state.idDisciplina
                }}
                  onChange={(choice) => { setIdDisciplina(choice.id) }} 
                  />
              </div>
              {cadastroError && <p className="text-red-600 text-xs mt-1">{cadastroError}</p>}
              {cadastroSucesso && <p className="text-green-500 text-xs mt-1">{cadastroSucesso}</p>}
            </div>
            <div>
              <button
                type="submit"
                className="flex w-full justify-center rounded-md bg-[#87001f] px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-[#ad0303] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Atualizar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}