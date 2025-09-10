import { Cookies } from "react-cookie";
import { AIEXEC_ACCESS_TOKEN } from "@/constants/constants";

export const customGetAccessToken = () => {
  const cookies = new Cookies();
  return cookies.get(AIEXEC_ACCESS_TOKEN);
};
