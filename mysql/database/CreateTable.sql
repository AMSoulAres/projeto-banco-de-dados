CREATE TABLE IF NOT EXISTS Professores 
( 
 idDepartamento INT,  
 nomeProfessor VARCHAR(40) NOT NULL DEFAULT 'NomeQualquer',  
 idProfessor INT PRIMARY KEY AUTO_INCREMENT, 
 idade INT
); 
CREATE TABLE IF NOT EXISTS Departamentos 
( 
 idDepartamento INT PRIMARY KEY AUTO_INCREMENT,  
 nomeDepartamento VARCHAR(80) NOT NULL, 
 endereco VARCHAR(255) NOT NULL
); 
CREATE TABLE IF NOT EXISTS Turmas 
( 
 idDisciplina INT,  
 idProfessor INT,  
 idTurma INT PRIMARY KEY AUTO_INCREMENT
); 
CREATE TABLE IF NOT EXISTS Disciplinas 
( 
 idDepartamento INT,  
 idDisciplina INT PRIMARY KEY AUTO_INCREMENT,
 nomeDisciplina VARCHAR(100) NOT NULL
); 
CREATE TABLE Estudantes 
( 
 matriculaEstudante INT PRIMARY KEY AUTO_INCREMENT,  
 email VARCHAR(40) DEFAULT 'mail@mail.com',  
 senha VARCHAR(15) NOT NULL,  
 curso VARCHAR(40) NOT NULL DEFAULT 'Curso Legal',  
 admin INT NOT NULL DEFAULT '0',  
 image MEDIUMBLOB
);
CREATE TABLE IF NOT EXISTS AvaliacaoProfessor 
( 
 matriculaEstudante INT,  
 idProfessor INT,  
 textoAvaliacao VARCHAR(255),  
 nivel INT NOT NULL,  
 idAvaliacaoProfessor INT PRIMARY KEY AUTO_INCREMENT  
); 
CREATE TABLE IF NOT EXISTS AvaliacaoTurma 
( 
 matriculaEstudante INT,  
 idTurma INT,  
 textoAvaliacao VARCHAR(255) NOT NULL,  
 nivel INT NOT NULL,  
 idAvaliacaoTurma INT PRIMARY KEY AUTO_INCREMENT  
); 
CREATE TABLE IF NOT EXISTS Denuncia 
( 
 idAvaliacaoProfessor INT,  
 idAvaliacaoTurma INT,  
 idDenuncia INT PRIMARY KEY AUTO_INCREMENT  
);
ALTER TABLE Professores ADD FOREIGN KEY(idDepartamento) REFERENCES Departamentos (idDepartamento);
ALTER TABLE Turmas ADD FOREIGN KEY(idDisciplina) REFERENCES Disciplinas (idDisciplina);
ALTER TABLE Turmas ADD FOREIGN KEY(idProfessor) REFERENCES Professores (idProfessor);
ALTER TABLE Disciplinas ADD FOREIGN KEY(idDepartamento) REFERENCES Departamentos (idDepartamento);
ALTER TABLE AvaliacaoProfessor ADD FOREIGN KEY(matriculaEstudante) REFERENCES Estudantes (matriculaEstudante);
ALTER TABLE AvaliacaoProfessor ADD FOREIGN KEY(idProfessor) REFERENCES Professores (idProfessor);
ALTER TABLE AvaliacaoTurma ADD FOREIGN KEY(matriculaEstudante) REFERENCES Estudantes (matriculaEstudante);
ALTER TABLE AvaliacaoTurma ADD FOREIGN KEY(idTurma) REFERENCES Turmas (idTurma);
ALTER TABLE Denuncia ADD FOREIGN KEY(idAvaliacaoProfessor) REFERENCES AvaliacaoProfessor (idAvaliacaoProfessor);
ALTER TABLE Denuncia ADD FOREIGN KEY(idAvaliacaoTurma) REFERENCES AvaliacaoTurma (idAvaliacaoTurma);
-- --------------------------------
-- INSERTS TEMPLATES
-- INSERT INTO `avaliacaounb`.`professores`
-- (`idDepartamento`,
-- `NomeProfessor`,
-- `idProfessor`)
-- VALUES
-- (<{idDepartamento: }>,
-- <{NomeProfessor: NomeQualquer}>,
-- <{idProfessor: }>);

-- INSERT INTO `avaliacaounb`.`departamentos`
-- (`NomeDepartamento`)
-- VALUES
-- (<{NomeDepartamento: }>);

-- INSERT INTO `avaliacaounb`.`disciplinas`
-- (`idDepartamento`,
-- `idDisciplina`)
-- VALUES
-- (<{idDepartamento: }>,
-- <{idDisciplina: }>);

-- INSERT INTO `avaliacaounb`.`turmas`
-- (`idDisciplina`,
-- `idProfessor`,
-- `idTurma`)
-- VALUES
-- (<{idDisciplina: }>,
-- <{idProfessor: }>,
-- <{idTurma: }>);

-- INSERT INTO `avaliacaounb`.`estudantes`
-- (`matriculaEstudante`,
-- `Email`,
-- `Senha`,
-- `Curso`)
-- VALUES
-- (<{matriculaEstudante: }>,
-- <{Email: mail@mail.com}>,
-- <{Senha: }>,
-- <{Curso: Curso Legal}>);

-- INSERT INTO `avaliacaounb`.`avaliacaoprofessor`
-- (`matriculaEstudante`,
-- `idProfessor`,
-- `TextoAvaliacao`,
-- `Nivel`,
-- `idAvaliacaoProfessor`)
-- VALUES
-- (<{matriculaEstudante: }>,
-- <{idProfessor: }>,
-- <{TextoAvaliacao: }>,
-- <{Nivel: }>,
-- <{idAvaliacaoProfessor: }>);

-- INSERT INTO `avaliacaounb`.`avaliacaoturma`
-- (`matriculaEstudante`,
-- `idTurma`,
-- `TextoAvaliacao`,
-- `Nivel`,
-- `idAvaliacaoTurma`)
-- VALUES
-- (<{matriculaEstudante: }>,
-- <{idTurma: }>,
-- <{TextoAvaliacao: }>,
-- <{Nivel: }>,
-- <{idAvaliacaoTurma: }>);

-- INSERT INTO `avaliacaounb`.`denuncia`
-- (`idAvaliacaoProfessor`,
-- `idAvaliacaoTurma`,
-- `idDenuncia`)
-- VALUES
-- (<{idAvaliacaoProfessor: }>,
-- <{idAvaliacaoTurma: }>,
-- <{idDenuncia: }>);