# DocuMaster

## Endpoints
- Frontend: `/`
- Upload: `/upload`
- List Documents: `/documents`
- Ask Question: `/ask`


## Pre-requisites
- Docker must be installed
- You need an OPENAI API KEY. Generate one at https://platform.openai.com/account/api-keys if you don't have it.

## Before you run
- Add your OPENAI API KEY to .env.example, following this format: OPENAI_API_KEY=your_openai_api_key
- Rename .env.example to .env

## How to Run:
- For the initial run: execute `docker compose up --build`
- For subsequent runs: execute `docker compose up`

- The API can be accessed at `http://localhost:8080`

NOTE: If you are using Compose V1, Use `docker-compose` instead of `docker compose`


## How to Run Tests
- Run `docker compose run app pytest`

## Pending Implementations
- The test scaffolding has been initialized but not fully implemented with test cases due to time constraint

## Notes on Potential Improvements and Additional Features
The following could not be implemented due to time constraint:

- Handle duplicate uploads by keeping state of document hash (using hashlib.sha256 to generate hash) and comparing document hashes in the upload endpoint function.
- Use a more robust ID system, such as ULID, instead of a randomly generated string from token.hex.
- Implement `S3Storage` and use as storage instead of `FileSystemStorage`. This will require installing `boto3`
- Implement a persistent vector store like Pinecone or PGVector instead of using FAISS.
- Persist conversation chain chat memory for subsequent conversation questions.
- Standardize `settings.SUPPORTED_FILE_TYPES` with an Enum data structure for consistency
- Include OPENAPI description for FASTAPI endpoints.
- Add CORSMiddleware middleware to FASTAPI app
- Implement error handling for potential conversation errors from the OpenAI server.
- Setup linting using flake8
