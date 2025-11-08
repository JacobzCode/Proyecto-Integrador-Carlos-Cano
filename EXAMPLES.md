# MoodKeeper - Examples

Register user:
```bash
curl -X POST http://localhost:8000/api/accounts -H "Content-Type: application/json" -d '{"handle":"juan","email":"juan@example.com","secret":"mipass"}'
```

Login:
```bash
curl -X POST http://localhost:8000/api/sessions -H "Content-Type: application/json" -d '{"handle":"juan","secret":"mipass"}'
```

Create entry:
```bash
curl -X POST http://localhost:8000/api/entries -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d '{"mood":6,"comment":"Me siento bien"}'
```
