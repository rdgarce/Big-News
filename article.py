from redis import Redis
from zlib import compress, decompress
from json import dumps, loads

class ATCqueue:
    def __init__(self, redis_conn : Redis):
        """
        Init the Reliable article queue with the given Redis connection
        """
        if not isinstance(redis_conn, Redis):
            raise ValueError("redis_conn can not be None!")
        self._r = redis_conn
    
    def list_len(self) -> int:
        return self._r.llen("articles")
    
    def BU_list_len(self) -> int:
        return self._r.llen("articles_backup")

    def push_batch(self, articles : list) -> int:
        """
        Push a batch of standardized articles to the reliable queue.
        Returns the length of the queue after the push
        """
        if not articles or not isinstance(articles, list):
            return

        cmprsd_batch = compress(dumps(articles).encode(), 9)
        return self._r.lpush("articles", cmprsd_batch)
    
    def pop_batch(self) -> (bytes | None, list | None):
        """
        Return a bytes field containing the reference of the batch and the articles batch itself
        as a list.
        This pop enables a reliable queue because popped element is pushed atomically in the backup queue.
        """
        cmprsd_batch = self._r.rpoplpush("articles", "articles_backup")
        if not cmprsd_batch:
            return (None, None)

        articles = decompress(cmprsd_batch).decode()
        articles = loads(articles)
        
        return cmprsd_batch, articles

    def peek_batch_from_BU(self) -> (bytes | None, list | None):
        """
        Peek (look without removing) and return a bytes field containing the reference 
        of the batch and the articles batch itself as a list.
        ATTENTION: This function is meant to be called ONLY by the ONE AND ONLY ONE node responsible
        for the look up of the backup queue.
        """
        cmprsd_batch = self._r.lrange("articles_backup", -1, -1)
        # We expect a list of one element or empty
        cmprsd_batch = cmprsd_batch[0] if cmprsd_batch else None
        if not cmprsd_batch:
            return (None, None)

        articles = decompress(cmprsd_batch).decode()
        articles = loads(articles)
        
        return cmprsd_batch, articles

    def del_batch_from_BU(self, batch_ref : bytes):
        """
        Delete the articles batch referred by the batch_ref from the backup queue.
        To be called by the Consumer after the processing of the articles is successfull.
        """
        if batch_ref:
            self._r.lrem("articles_backup", 1, batch_ref)
