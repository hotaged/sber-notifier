class __IdCounter:
    count: int = 0

    @classmethod
    def count_id(cls) -> str:
        cls.count += 1
        return str(cls.count)


unique_query_id = __IdCounter.count_id
