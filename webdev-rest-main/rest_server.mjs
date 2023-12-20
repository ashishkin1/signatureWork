import * as path from 'node:path';
import * as url from 'node:url';

import { default as express } from 'express';
import { default as sqlite3 } from 'sqlite3';
import { execPath } from 'node:process';
import { default as cors } from 'cors';

const __dirname = path.dirname(url.fileURLToPath(import.meta.url));
const db_filename = path.join(__dirname, 'db', 'stpaul_crime.sqlite3');

const port = 8000;

let app = express();
app.use(cors());
app.use(express.json());

/********************************************************************
 ***   DATABASE FUNCTIONS                                         ***
 ********************************************************************/
// Open SQLite3 database (in read-write mode)
let db = new sqlite3.Database(db_filename, sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.log('Error opening ' + path.basename(db_filename));
    }
    else {
        console.log('Now connected to ' + path.basename(db_filename));
    }
});

// Create Promise for SQLite3 database SELECT query
function dbSelect(query, params) {
    return new Promise((resolve, reject) => {
        db.all(query, params, (err, rows) => {
            if (err) {
                reject(err);
            }
            else {
                resolve(rows);
            }
        });
    });
}

// Create Promise for SQLite3 database INSERT or DELETE query
function dbRun(query, params) {
    return new Promise((resolve, reject) => {
        db.run(query, params, (err) => {
            if (err) {
                reject(err);
            }
            else {
                resolve();
            }
        });
    });
}

/********************************************************************
 ***   REST REQUEST HANDLERS                                      ***
 ********************************************************************/
// GET request handler for crime codes
app.get('/codes', (req, res) => {
    try {
        let query = 'SELECT * FROM Codes';
        let params = [];

        // Check if the 'code' query parameter is provided
        if (req.query.code) {
            const codeList = req.query.code.split(',').map(Number);
            query += ' WHERE code IN (' + codeList.map(() => '?').join(',') + ')';
            params = codeList;
        }

        query += ' ORDER BY code';

        // Execute the query synchronously
        db.all(query, params, (err, rows) => {
            if (err) {
                console.error(err);
                res.status(500).send('Internal Server Error');
            } else {
                res.status(200).type('json').send(rows);
            }
        });
    } catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
    }
});




// GET request handler for neighborhoods
app.get('/neighborhoods', (req, res) => {
    const neighborhoodIds = req.query.id; // Assuming it's a comma-separated list

    let query = 'SELECT * FROM Neighborhoods';

    if (neighborhoodIds) {
        const idsArray = neighborhoodIds.split(',').map(Number);
        query += ` WHERE neighborhood_number IN (${idsArray.join(',')})`;
    }

    db.all(query, [], (err, neighborhoods) => {
        if (err) {
            console.error(err);
            res.status(500).send('Internal Server Error');
        } else {
            // Sort neighborhoods by id
            neighborhoods.sort((a, b) => a.neighborhood_number - b.neighborhood_number);

            const result = neighborhoods.map(({ neighborhood_number, neighborhood_name }) => ({
                id: neighborhood_number,
                name: neighborhood_name,
            }));

            res.status(200).type('json').send(result);
        }
    });
});

// GET request handler for crime incidents
// Endpoint to retrieve incidents with optional filters
app.get('/incidents', (req, res) => {
    // Base query with no filters
    let query = 'SELECT case_number, DATE(date_time) AS date, TIME(date_time) as time, code, incident, police_grid, neighborhood_number, block FROM Incidents';

    let params = [];

    let count = 0;

    let limit = 1000;

    if (req.query.hasOwnProperty('code')) {
        if (count > 0) {
            query += " AND ";
        } else {
            query += " WHERE ";
        }
        let codes = req.query.code.split(',');
        query += "code IN (";
        codes.forEach((element, index) => {
            query += '?'
            if (index < codes.length-1) {
                query += ','
            }
            params.push(parseInt(element));
        });
        query += ")";
        count++;
    }

    if (req.query.hasOwnProperty('grid')) {
        if (count > 0) {
            query += " AND ";
        } else {
            query += " WHERE ";
        }
        let grids = req.query.grid.split(',');
        query += "police_grid IN (";
        grids.forEach((element, index) => {
            query += '?'
            if (index < grids.length-1) {
                query += ','
            }
            params.push(parseInt(element));
        });
        query += ")";
        count++;
    }

    if (req.query.hasOwnProperty('neighborhood')) {
        if (count > 0) {
            query += " AND ";
        } else {
            query += " WHERE ";
        }
        let neighborhoods = req.query.neighborhood.split(',');
        query += "neighborhood_number IN (";
        neighborhoods.forEach((element, index) => {
            query += '?'
            if (index < neighborhoods.length-1) {
                query += ','
            }
            params.push(parseInt(element));
        });
        query += ")";
        count++;
    }

    if (req.query.hasOwnProperty('start_date')) {
        if (count > 0) {
            query += " AND ";
        } else {
            query += " WHERE ";
        }
        query += "date_time >= ?";
        params.push(req.query.start_date +"T00:00:00")
        count++;
    }
    if (req.query.hasOwnProperty('end_date')) {
        if (count > 0) {
            query += " AND ";
        } else {
            query += " WHERE ";
        }
        query += "date_time <= ?";
        params.push(req.query.end_date +"T23:59:59");
        count++;
    }

    query += ' ORDER By date_time DESC'
   
    if (req.query.hasOwnProperty('limit')) {
        limit = req.query.limit;
    }
    query += " LIMIT " + limit;


    console.log('Final Query:', query);
    console.log(params);

    dbSelect(query, params)
        .then((rows) => {
            console.log('hit');
            res.status(200).type('json').send(rows);
        })
        .catch((error) => {
            console.log('miss');
            res.status(500).type('txt').send(error);
        });
});

/*
"{\"case_number\": \"21174014\", \"date\": \"2021-08-22\", \"time\": \"17:46:00\", \"code\": 9954, \"incident\": \"Proactive Police Visit\", \"police_grid\": 194, \"neighborhood_number\": 3, \"block\": \"1XX CESARCHAVEZ ST\"}"

*/

// PUT request handler for new crime incident
app.put('/new-incident', (req, res) => {
    const { case_number, date, time, code, police_grid, neighborhood_number, block } = req.body;

    if (!date || !time || !code || !police_grid || !neighborhood_number || !block) {
        res.status(400).json({ error: 'Missing required fields in the request body' });
        return;
    }

    const query = 'INSERT INTO incidents (case_number, date_time, code, police_grid, neighborhood_number, block) VALUES (?, ?, ?, ?, ?, ?)';
    const params = [case_number, date + "T"+time, code, police_grid, neighborhood_number, block];

    dbRun(query, params)
        .then(() => {
            res.status(200).json({ message: 'Incident added successfully' });
        })
        .catch((error) => {
            res.status(500).json({ error: error.message });
        });
});


// DELETE request handler for new crime incident
app.delete('/remove-incident', (req, res) => {
    const caseNumber = req.body.case_number;

    const query = 'DELETE FROM Incidents WHERE case_number = ?';
    const params = [caseNumber];

    console.log('Delete Query:', query);
    dbSelect('SELECT * FROM Incidents WHERE case_number = ?', params)
    .then((rows)=> {
        console.log(rows);
        if (rows.length == 0) {
            throw 'error case number does not exist';
        } else {
            return dbRun(query, params);
        }
    })
    .then(() => {
        console.log('Incident Removed');
        res.status(200).json({ message: 'Incident removed successfully' });
    })
    .catch((error) => {
        console.error('Error removing incident:', error);
        res.status(500).json({ error: error });
    });

    console.log('Query Parameters:', params);
});

/********************************************************************
 ***   START SERVER                                               ***
 ********************************************************************/
// Start server - listen for client connections
app.listen(port, () => {
    console.log('Now listening on port ' + port);
});
