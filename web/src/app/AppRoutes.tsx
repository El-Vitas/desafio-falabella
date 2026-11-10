import { Navigate, Route, Routes } from "react-router";

import { ItemPage } from "../pokemon/pages/ItemPage";
import { ItemsPage } from "../pokemon/pages/ItemsPage";
import { ROUTES } from "../shared/constants/routes";
import { NotFoundPage } from "../shared/ui/NotFoundPage";
import { StatsPage } from "../stats/StatsPage";
import { AppLayout } from "./AppLayout";

export const AppRoutes = () => (
  <Routes>
    <Route element={<AppLayout />}>
      <Route path={ROUTES.home} element={<Navigate to={ROUTES.items} replace />} />
      <Route path={ROUTES.items} element={<ItemsPage />} />
      <Route path={ROUTES.item} element={<ItemPage />} />
      <Route path={ROUTES.queries} element={<StatsPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Route>
  </Routes>
);
