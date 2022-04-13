import { BaseAPI } from "../_base";
import { CenaAnalytics } from "~/types/api-types/analytics";

const prefix = "/api";

const routes = {
  base: `${prefix}/admin/analytics`,
};

export class AdminAnalyticsApi extends BaseAPI {
  async getAnalytics() {
    return await this.requests.get<CenaAnalytics>(routes.base);
  }
}
