| **Change**                                                            | **Why It Was Done**                                                                       
| --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- 
| Used `?` placeholders instead of `f""` in SQL queries           | Prevents SQL injection, a critical security flaw.                                     
| Hashed passwords with bcrypt                                   | Never store plaintext passwords; hashing protects user data even if the DB is leaked. 
| Used `request.get_json()` with `try/except`                    | Prevents app from crashing if request body is missing or malformed.                       
| Returned `jsonify()` + HTTP status codes                       | Follows RESTful API standards and improves client-side error handling.                
| Returned 400 for bad input, 404 for not found, 201 for creation | Correct HTTP response semantics improve API clarity and usability.                        
| Sanitized string inputs for search                             | Prevents SQL injection via `LIKE '%term%'`.                                               
| Removed printing to console in production endpoints             | Not needed in deployed APIs and clutters logs.                                            
| Removed fetching and exposing password hashes                   | Avoids leaking internal data to clients.                                                  
| Renamed routes and functions for clarity                        | Improves readability and maintainability.                                                 
|Added `int:` in route parameters                               | Flask handles type conversion and avoids unsafe string comparisons.                       
