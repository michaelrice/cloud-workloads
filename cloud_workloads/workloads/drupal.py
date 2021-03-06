from cloud_workloads.common.gatling.workload import Workload as GatlingWorkload


class Workload(GatlingWorkload):
    """
    Class that handles a drupal cloud workload.
    """

    DEFAULT_STATES = {
        'drupal_mysql_master': ['drupal.db_master'],
        'drupal_mysql_slave': ['drupal.db_slave'],
        'drupal_web': ['drupal.web'],
        'drupal_gatling': ['drupal.gatling']
    }

    DEFAULT_ANTI_STATES = {
        'drupal_mysql_master': ['drupal.antidb_master'],
        'drupal_mysql_slave': ['drupal.antidb_slave'],
        'drupal_web': ['drupal.antiweb'],
        'drupal_gatling': ['drupal.antigatling']
    }

    DEFAULT_CONFIG = {
        'gatling_dir': 'gatling',
        'webhead_url': 'http://%s',
        'webhead_role': 'drupal_web',
        'gatling_role': 'drupal_gatling',
        'gatling_user': 'gatling',
        'duration': '90',
        'users_start': '500',
        'users_step': '200'
    }

    DEPLOY_SEQUENCE = [
        {'state': 'drupal.db_master',
         'next': {'state': 'drupal.db_slave'}},
        {'state': 'drupal.web'},
        {'state': 'drupal.gatling'}
    ]

    UNDEPLOY_SEQUENCE = [
        {'state': 'drupal.antidb_master'},
        {'state': 'drupal.antidb_slave'},
        {'state': 'drupal.antiweb'},
        {'state': 'drupal.antigatling'}
    ]

    MINION_GRAPH_EDGE_MAP = {
        'drupal_gatling': ['drupal_web'],
        'drupal_web': ['drupal_mysql_master', 'drupal_mysql_slave'],
        'drupal_mysql_slave': ['drupal_mysql_master']
    }

    @property
    def name(self):
        """
        Returns name of the workload.

        :returns: String name of the workload
        """
        return 'Drupal'

    def command(self):
        """
        Assembles the command that would be run via command line.

        :returns: String
        """
        return super(Workload, self).command('drupal.UserSimulation')

    def data(self):
        if not self.data_dict.get('exception_trace'):
            run = self.best_run
            active_sessions_plot = run['stats'].sessions_per_second_plot
            self.data_dict.update({
                'users': run.users,
                'duration': run.duration,
                'mean_response_time': run.mean_response_time,
                'requests_per_second_plot':
                run['stats'].requests_per_second_plot,
                'active_sessions_per_second_plot': active_sessions_plot,
                'response_times_plot': run['stats'].response_times_plot
            })
        return self.data_dict
