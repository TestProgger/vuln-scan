import { types } from "mobx-state-tree";
import createPersistentStore from "mst-persistent-store";
import { UserStore } from "./user";
import { INITIAL_USER, INITIAL_TOKEN, INITIAL_ERROR } from "./consts";
import { TokenStore } from "./token";
import { ErrorStore } from "./error";

const RootStore = types.model("RootStore", {
  user: types.optional(UserStore, INITIAL_USER),
  error: types.optional(ErrorStore, INITIAL_ERROR),
  token: types.optional(TokenStore, INITIAL_TOKEN)
})
.actions(self => ({
  logout(){
    self.user.removeUser()
    self.token.removeToken()
  }
}))


export const [PersistentStoreProvider, usePersistentStore] =
  createPersistentStore(RootStore, {}, {}, { writeDelay: 100, logging: false });