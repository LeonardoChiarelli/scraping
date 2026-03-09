class CleaningPipeline:

    def process_item(self, item, spider):

        if item.get("price"):

            price = item["price"]

            price = price.replace("R$", "")
            price = price.replace(",", ".")

            item["price"] = price.strip()

        return item