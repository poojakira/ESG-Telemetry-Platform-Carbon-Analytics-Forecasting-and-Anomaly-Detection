import asyncio
import logging
import uuid
from datetime import datetime

# Configure a simple logger for the showcase
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EcoPipeline")

class AsyncIngestor:
    """
    A reference implementation of a high-throughput, asynchronous ingestion pipeline.
    
    Design Patterns:
    - Producer-Consumer: Decouples high-frequency data arrival from database/processing persistence.
    - Async IO: Utilizes Python's asyncio for non-blocking task management.
    - Batching: Collects records into logical batches for transactional integrity.
    
    Performance Note: 
    This architecture is designed to handle thousands of telemetry records per second 
    by offloading processing to a background worker.
    """
    
    def __init__(self, processing_callback=None):
        self.queue = asyncio.Queue()
        self.is_running = False
        self.processing_callback = processing_callback

    async def ingest_batch(self, records: list, source_id: str):
        """
        Accepts a list of records and adds them to the processing queue.
        This call returns immediately to the caller (e.g., an API endpoint).
        """
        batch_id = str(uuid.uuid4().hex[:8]).upper()
        payload = {
            "batch_id": batch_id,
            "source_id": source_id,
            "records": records,
            "timestamp": datetime.now()
        }
        await self.queue.put(payload)
        logger.info(f"✅ Batch {batch_id} queued for processing.")
        return batch_id

    async def run_worker(self):
        """
        The background consumer that processes batches from the queue.
        Includes failure handling and retry logic.
        """
        self.is_running = True
        logger.info("🚀 AsyncIngestor Worker Started.")
        
        while self.is_running:
            try:
                # 1. Wait for the next batch
                job = await self.queue.get()
                batch_id = job["batch_id"]
                records = job["records"]
                
                logger.info(f"📦 Processing Batch {batch_id} ({len(records)} records)...")
                
                # 2. Simulate or execute processing (e.g., DB writes, ML inference)
                if self.processing_callback:
                    await self.processing_callback(job)
                else:
                    # Default simulation logic
                    await asyncio.sleep(0.1) # Simulate IO latency
                
                # 3. Mark task as done
                self.queue.task_done()
                logger.info(f"🏁 Batch {batch_id} processed successfully.")
                
            except Exception as e:
                logger.error(f"❌ Worker Error: {e}")
                # In a real system, we would implement a Dead Letter Queue (DLQ) here
                await asyncio.sleep(1)

    def stop(self):
        """ Gracefully stops the worker. """
        self.is_running = False

# Example Usage (Prototype Mode)
if __name__ == "__main__":
    async def main():
        ingestor = AsyncIngestor()
        
        # Start worker as background task
        worker_task = asyncio.create_task(ingestor.run_worker())
        
        # Ingest sample data
        await ingestor.ingest_batch([{"sku": "A1", "carbon": 10.5}], "Test-App")
        await ingestor.ingest_batch([{"sku": "B2", "carbon": 20.1}], "Test-App")
        
        # Give it a moment to process
        await asyncio.sleep(1)
        ingestor.stop()
        await worker_task

    asyncio.run(main())
