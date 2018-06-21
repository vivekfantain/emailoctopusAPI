from EmailOctopus import Campaigns


class CampaignReport(Campaigns):
    def iter_failed_emails(self, campaign):
        for item in self.iter_bounced(campaign):
            if item['type'] == 'HARD':
                yield item['contact']['email_address']

        for item in self.iter_unsubscribed(campaign):
            yield item['contact']['email_address']

        for item in self.iter_complained(campaign):
            yield item['contact']['email_address']
