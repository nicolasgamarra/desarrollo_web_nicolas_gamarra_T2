CREATE TABLE IF NOT EXISTS comentario (
  id INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  texto VARCHAR(500) NOT NULL,
  fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actividad_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX fk_comentario_actividad_idx (actividad_id ASC),
  CONSTRAINT fk_comentario_actividad
    FOREIGN KEY (actividad_id)
    REFERENCES actividad (id)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
) ENGINE = InnoDB;


