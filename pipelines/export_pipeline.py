from storage.json_exporter import JSONExporter


class ExportPipeline:

    def open_spider(self, spider):

        self.exporter = JSONExporter("products.json")

    def close_spider(self, spider):

        self.exporter.close()

    def process_item(self, item, spider):

        self.exporter.export(item)

        return item