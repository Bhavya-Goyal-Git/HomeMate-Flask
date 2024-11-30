# HomeMate - IITM MAD2 Project
### Term September 2024
A full stack project made using Python (flask) and Vue.js, a web platform where **Service Professionals** and **Customers** can register and discover each other.  

For project details, database schema, implementations, check out *HomeMateProjectReport.pdf*

**To run the Project:**  

Dependencies: *npm, python, redis, mailhog*

```bash
sh local_setup.sh
sh local_run.sh
sh frontend_run.sh
```

**To run backend asynchronous jobs:**

Run MailHog first: `MailHog`  
Then in separate processes, run:

```bash
sh local_worker.sh
sh local_beat.sh
```