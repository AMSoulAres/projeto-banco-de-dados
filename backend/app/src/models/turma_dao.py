from fastapi.exceptions import HTTPException
from pydantic import BaseModel

class Turma:
    def __init__(self, idDisciplina, idTurma, idProfessor):
        self.idDisciplina = idDisciplina
        self.idProfessor = idProfessor
        self.idTurma = idTurma

class TurmaContexto:
    def __init__(self, nomeDisciplina, idDisciplina, nomeProfessor, idProfessor, idTurma):
        self.nomeDisciplina = nomeDisciplina
        self.idDisciplina = idDisciplina
        self.nomeProfessor = nomeProfessor
        self.idProfessor = idProfessor
        self.idTurma = idTurma

class TurmaPost(BaseModel):
    idProfessor: int
    idDisciplina: int 

class TurmaUpdate(BaseModel):
    idProfessor: int
    idDisciplina: int 

class TurmaDeleteRequest(BaseModel):
    idTurma: int
    matriculaEstudanteLogado: int
class TurmaDao:
    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor
    
    def get_all(self):
        try:
            self.cursor.execute("SELECT * FROM avaliacaounb.Turmas")
            resposta = self.cursor.fetchall()
            print(resposta)
            turmas = [Turma(*turma) for turma in resposta]
            return turmas
        except Exception as err:
            print(err)
            raise err
    
    def get_all_context(self):
        try:
            query = "SELECT d.nomeDisciplina, d.idDisciplina, p.nomeProfessor, p.idProfessor, t.idTurma "
            query += "FROM avaliacaounb.Turmas t "
            query += "INNER JOIN avaliacaounb.Professores p "
            query += "ON t.idProfessor = p.idProfessor "
            query += "INNER JOIN avaliacaounb.Disciplinas d "
            query += "ON t.idDisciplina = d.idDisciplina; "
            self.cursor.execute(query)
            resposta = self.cursor.fetchall()
            turmas = [TurmaContexto(*turma) for turma in resposta]
            return turmas
        
        except Exception as err:
            print(err)
            raise err
    
    def get_turma_por_id(self, idTurma):
        try:
            self.cursor.execute(f"SELECT * FROM avaliacaounb.Turmas WHERE idTurma = {idTurma}")
            resposta = self.cursor.fetchone()
            if resposta is None:
                raise HTTPException(status_code=404)
            
            turma = Turma(*resposta)

            return turma
        except Exception as err:
            print(err)
            raise err
        
    def get_turma_por_id_contextualizada(self, idTurma):
        try:
            query = "SELECT d.nomeDisciplina, d.idDisciplina, p.nomeProfessor, p.idProfessor, t.idTurma "
            query += "FROM avaliacaounb.Turmas t "
            query += "INNER JOIN avaliacaounb.Professores p "
            query += "ON t.idProfessor = p.idProfessor "
            query += "INNER JOIN avaliacaounb.Disciplinas d "
            query += f"ON t.idDisciplina = d.idDisciplina WHERE t.idTurma = {idTurma} "
            self.cursor.execute(query)
            resposta = self.cursor.fetchone()
            if resposta is None:
                raise HTTPException(status_code=404)
            
            turma = TurmaContexto(*resposta)

            return turma
        except Exception as err:
            print(err)
            raise err
    
    def add_turma(self, idProfessor, idDisciplina):
        try:
            if (idProfessor != 0 or idDisciplina != 0):
                existeTurmaQuery = "SELECT idDisciplina, idProfessor FROM avaliacaounb.Turmas "
                existeTurmaQuery += f"WHERE idDisciplina = {idDisciplina} AND idProfessor = {idProfessor};"
                self.cursor.execute(existeTurmaQuery)
                listaTurmas = self.cursor.fetchall()
                print(listaTurmas)
                if listaTurmas == []:
                    self.cursor.execute(f"SELECT idDepartamento FROM avaliacaounb.Professores WHERE idProfessor = {idProfessor}")
                    departamentoProfessor = self.cursor.fetchone()[0]

                    self.cursor.execute(f"SELECT idDepartamento FROM avaliacaounb.Disciplinas WHERE idDisciplina = {idDisciplina}")
                    departamentoDisciplina = self.cursor.fetchone()[0]

                    if departamentoProfessor == departamentoDisciplina:
                        self.cursor.execute(f"INSERT INTO avaliacaounb.Turmas (idDisciplina, idProfessor) VALUES ({idDisciplina}, {idProfessor});")
                        self.db.commit()
                        self.cursor.execute("SELECT LAST_INSERT_ID();")
                        estudanteInserido = self.cursor.fetchone()
                        return estudanteInserido
                    raise HTTPException(status_code=400, detail="Professor e Disciplina devem pertencer ao mesmo departamento")
                
                raise HTTPException(status_code=409, detail="Turma já cadastrada")
            raise HTTPException(status_code=400, detail="Valores não podem ser vazios")
            
        except Exception as err:
            print(err)
            raise err

    def update_turma(self, idTurma, idProfessor, idDisciplina):
        try:
            self.cursor.execute(f"SELECT idDepartamento FROM avaliacaounb.Professores WHERE idProfessor = {idProfessor}")
            departamentoProfessor = self.cursor.fetchone()[0]
            print(departamentoProfessor)

            self.cursor.execute(f"SELECT idDepartamento FROM avaliacaounb.Disciplinas WHERE idDisciplina = {idDisciplina}")
            departamentoDisciplina = self.cursor.fetchone()[0]
            print(departamentoDisciplina)

            if departamentoProfessor == departamentoDisciplina:
                self.cursor.execute(f"UPDATE avaliacaounb.Turmas SET idProfessor = {idProfessor} WHERE idTurma = {idTurma}")
                self.db.commit()
                return
            raise HTTPException(status_code=400, detail="Professor e Disciplina devem pertencer ao mesmo departamento")
        

        except Exception as err:
            print(err)
            raise err
    
    def delete_turma(self, idTurma, matriculaEstudante):
        try:
            self.cursor.execute(f"SELECT * FROM avaliacaounb.Turmas WHERE idTurma = {idTurma}")
            turma = self.cursor.fetchone()
            if turma is None:
                raise HTTPException(status_code=404, detail="Turma não encontrada")

            self.cursor.execute(f"SELECT admin FROM avaliacaounb.Estudantes WHERE matriculaEstudante = {matriculaEstudante}")
            admin = self.cursor.fetchone()

            if admin is None:
                raise HTTPException(status_code=404, detail="Estudante não cadastrado")
            admin = admin[0]

            if admin == 1:
                self.cursor.execute(f"SELECT idAvaliacaoTurma FROM avaliacaounb.AvaliacaoTurma at2 WHERE at2.idTurma = {idTurma};")
                idAvaliacoes = self.cursor.fetchall()

                for id in idAvaliacoes:
                    self.cursor.execute(f"DELETE FROM avaliacaounb.Denuncia WHERE  idAvaliacaoTurma = {id[0]}")
                    self.db.commit()

                self.cursor.execute(f"DELETE FROM avaliacaounb.AvaliacaoTurma at2 WHERE at2.idTurma = {idTurma};") 
                self.db.commit()
                self.cursor.execute(f"DELETE FROM avaliacaounb.Turmas WHERE idTurma = {idTurma};")
                self.db.commit()
                return

            raise HTTPException(status_code=403, detail="Estudante não é administrador")

        except Exception as err:
            print(err)
            raise err
    