
class view_mysql:
    route_app_labels = {'urban_app'}  # app name

    def db_for_read(self, model, **hints):
        # print('self', self)

        if model._meta.app_label in self.route_app_labels:
            # print('model._meta', model._meta)
            # print('model._meta.app_label', model._meta.app_label)
            # print('self.route_app_labels', self.route_app_labels)
            return 'mysql_views_db'
        return None

    def db_for_write(self, model, **hints):

        if model._meta.app_label in self.route_app_labels:
            return 'mysql_views_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if app_label in self.route_app_labels:
            return db == 'mysql_views_db'
        return None


