# Copyright (c) 2016-2018 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import hashlib


class CallJob(object):
    """
    Base class for jobs that call SUTs and can find new issues.
    """

    def __init__(self, id, config, db, listener):
        self.id = id
        self.config = config
        self.db = db
        self.listener = listener
        # expects self.sut_name and self.fuzzer_name to be set by descendants

    def add_issue(self, issue, new_issues):
        test = issue['test']

        # Save issue details.
        issue.update(dict(sut=self.sut_name,
                          fuzzer=self.fuzzer_name,
                          test=test,
                          reduced=None,
                          reported=False))

        # Generate default hash ID for the test if does not exist.
        if 'id' not in issue or not issue['id']:
            hasher = hashlib.md5()
            hasher.update(test if isinstance(test, bytes) else str(test).encode('utf-8'))
            issue['id'] = hasher.hexdigest()

        # Save new issues.
        if self.db.add_issue(issue):
            new_issues.append(issue)
            self.listener.new_issue(issue=issue)
        else:
            self.listener.update_issue(issue=issue)
