# Cloud Price Comparison Tool
This project is a Django Rest Framework (DRF) application that provides an API for comparing cloud service prices across different cloud service providers (AWS, GCP, etc.). Users can filter instances based on criteria such as CPU count, RAM, and location. Services are grouped based on the combination of CPU and RAM.

## Requirements

- Docker

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/cmaliwal/digiusher_assignment.git
    cd digiusher_assignment
    ```

2. Build the Flask application Docker image:

    ```bash
    docker compose build
    ```

3. Run the application locally:

    ```bash
    docker compose up
    ```

4. Access the bash(optional):

    ```bash
    docker compose ps
    ```

    ```bash
    docker exec -it container_id /bin/bash
    ```

## API Endpoints

The primary API endpoint for retrieving cloud instance prices is as follows:

### **1. Cloud Instance Price List**

- **URL**: `/api/cloud-instances/`
- **Method**: `GET`
- **Description**: Retrieves cloud instances grouped by CPU and RAM. You can filter results using various parameters.

### Query Parameters:

- `cloud_type`: Filter by cloud provider (e.g., `aws`, `gcp`, etc.).
- `location`: Filter by location/region (e.g., `us-east-1`).
- `min_vcpu`: Filter by minimum number of CPUs.
- `max_vcpu`: Filter by maximum number of CPUs.
- `min_ram_gb`: Filter by minimum RAM (in GB).
- `max_ram_gb`: Filter by maximum RAM (in GB).
- `page`: Page number for pagination.
- `page_size`: Number of results per page.

### Example Request:


Here is the API Endpoints section formatted for VS Code, using Markdown syntax:

markdown
Copy code
## API Endpoints

The primary API endpoint for retrieving cloud instance prices is as follows:

### **1. Cloud Instance Price List**

- **URL**: `/api/cloud-instances/`
- **Method**: `GET`
- **Description**: Retrieves cloud instances grouped by CPU and RAM. You can filter results using various parameters.

### Query Parameters:

- `cloud_type`: Filter by cloud provider (e.g., `aws`, `gcp`, etc.).
- `location`: Filter by location/region (e.g., `us-east-1`).
- `min_vcpu`: Filter by minimum number of CPUs.
- `max_vcpu`: Filter by maximum number of CPUs.
- `min_ram_gb`: Filter by minimum RAM (in GB).
- `max_ram_gb`: Filter by maximum RAM (in GB).
- `page`: Page number for pagination.
- `page_size`: Number of results per page.

### Example Request:

#### GET /api/cloud-instances/?cloud_type=aws&min_vcpu=4&max_ram_gb=8

#### Response

```json
[
    {
        "vcpu": 4,
        "ram_gb": 4.0,
        "instance_count": 3,
        "instances": [
            {
                "cloud_type": "aws",
                "location": "us-east-1",
                "instance_type": "t2.medium",
                "instance_family": "Storage optimized"
                "vcpu": 4,
                "ram_gb": 4.0,
                "price_per_hour": 0.0464,
                "effective_date": "2023-10-04"
            },
            {
                "cloud_type": "gcp",
                "location": "us-east-1",
                "instance_type": "n1-standard-2",
                "instance_family": "Storage optimized"
                "vcpu": 4,
                "ram_gb": 4.0,
                "price_per_hour": 0.0500,
                "effective_date": "2023-10-04"
            }
        ]
    },
    {
        "vcpu": 4,
        "ram_gb": 6.0,
        "instance_count": 2,
        "instances": [
            {
                "cloud_type": "aws",
                "location": "us-west-1",
                "instance_type": "t2.large",
                "instance_family": "Storage optimized"
                "vcpu": 4,
                "ram_gb": 6.0,
                "price_per_hour": 0.0928,
                "effective_date": "2023-10-04"
            }
        ]
    }
]
```

## Pagination

The API supports pagination to efficiently handle large datasets. Pagination is enabled by default with 10 results per page.

### Pagination Parameters:

- `page`: The page number to retrieve.
- `page_size`: Number of items per page (default is 10).

### Example Paginated Request:

#### GET /api/cloud-instances/?page=2&page_size=5


### Example Paginated Response:

```json
{
    "count": 20,
    "next": "http://localhost:8000/api/cloud-instances/?page=3",
    "previous": "http://localhost:8000/api/cloud-instances/?page=1",
    "results": [
        {
            "id": 6
            "cloud_type": "aws",
            "location": "us-east-1",
            "instance_type": "t2.medium",
            "instance_family": "Storage optimized"
            "vcpu": 4,
            "ram_gb": 4.0,
            "price_per_hour": 0.0464,
            "effective_date": "2023-10-04"
        }
    ]
}
```

## Future Scope of Improvement

### 1. **Support for Additional Cloud Providers**
   - Expand to include Azure, IBM Cloud, Oracle Cloud, and others to broaden comparison options.

### 2. **Real-Time Price Updates**
   - Implement real-time price fetching using asynchronous tasks with Celery and Redis for up-to-date pricing.

### 3. **Cost Optimization Suggestions**
   - Provide recommendations for optimal cloud instances based on user needs, such as best cost-per-performance ratio.

### 4. **Support for Reserved and Spot Instances**
   - Add support for reserved and spot instances to offer more pricing models for cost-effective options.

### 5. **User Authentication and Custom Preferences**
   - Allow users to log in and save their preferred filtering settings and configurations for future use.

### 6. **Enhanced Filtering Options**
   - Introduce more filters like storage type, network bandwidth, GPU support, and operating system for better matching of user requirements.

### 7. **Historical Price Tracking**
   - Track and display historical cloud instance prices to help users analyze price trends and optimize future costs.

### 8. **Frontend Integration**
   - Build a frontend (e.g., using React or Vue) to provide a user-friendly interface for comparing cloud instances visually.
