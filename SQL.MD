# SQL

### Marco o Frame
```sql
LAST_VALUE(City) OVER(
    ORDER BY year asc
    RANGE BETWEEN 
    UNBOUNDED PRECEDING AND
    UNBOUNDED FOLLOWING
) as LAST_CITY
```  

RANGE y ROW se usan para especificar que hacer con los "empates". 
- Por defecto un marco comienza en el principio de la tabla y termina en la fila actual, de ahi que se necesite especificar un marco diferente.
- RANGE trata los empates como una sola fila. Ej:
    - sum + range, los empates se suman y luego se muestra el resultado de su suma.

        |year|medals|
        |----|------|
        |2000|  10  |
        |2001|  10  |
        |2001|  10  |

        |year|medals|sum|
        |----|------|---|
        |2000|  10  | 10|
        |2001|  10  | 30|
        |2001|  10  | 30|

    - sum + row
        |year|medals|sum|
        |----|------|---|
        |2000|  10  | 10|
        |2001|  10  | 20|
        |2001|  10  | 30|


```sql
ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
--Abarca 4 filas 3 + 1
ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING

ROWS BETWEEN CURRENT ROW AND 3 FOLLOWING
```

```sql
-- Create the correct extension to enable CROSSTAB
CREATE EXTENSION IF NOT EXISTS tablefunc;

SELECT * FROM CROSSTAB($$
  WITH Country_Awards AS (
    SELECT
      Country,
      Year,
      COUNT(*) AS Awards
    FROM Summer_Medals
    WHERE
      Country IN ('FRA', 'GBR', 'GER')
      AND Year IN (2004, 2008, 2012)
      AND Medal = 'Gold'
    GROUP BY Country, Year)

  SELECT
    Country,
    Year,
    RANK() OVER
      (PARTITION BY Year
       ORDER BY Awards DESC) :: INTEGER AS rank
  FROM Country_Awards
  ORDER BY Country ASC, Year ASC;
-- Fill in the correct column names for the pivoted table
$$) AS ct (Country VARCHAR,
           "2004" INTEGER,
           "2008" INTEGER,
           "2012" INTEGER)

Order by Country ASC;
```

## Tipos de datos
- Texto: 
    - `CHAR`, `VARCHAR`, `TEXT`
- NUMERICO
    - `INT`, `DECIMAL`
- FECHA
    - `DATE`, `DATETIME`, `TIMESTAMP`, `INTERVAL`

Tabla de Interés:  
    `INFORMATION_SCHEMA.COLUMNS`