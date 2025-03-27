# gklm-chatbot

The solution presented here is the integration of IBM’s watsonx Assistant with GKLM, allowing users to manage keys, check server health, verify backups, retrieve user details, and even address common configuration questions—all through a simple, natural language chat interface. This chatbot will serve as a virtual assistant that interacts directly with the GKLM console, enhancing the user experience and providing security professionals and administrators with a more efficient way to perform tasks.

It involves developing a chat assistant using which user can get the gklm server details including key management, server configurations, backup and restore options and user management. In the same chatbot user can also get the general details as REST API's, license information and other information that is available in IBM documentation about gklm.


This repo contains two main folder.

    1. chatbot-rag folder contains the RAG implementation for IBM documents available for GKLM.
    2. chatbot-usermanagement handles the REST API's for user management which is consumed in assistant.

Remaining are OpenAPI files for integrating different cases with watsonx assistant.