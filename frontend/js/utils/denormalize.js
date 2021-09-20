import { denormalize } from 'normalizr';

import { battlesSchema, battleSchema } from './schema';

export const denormalizeBattleData = (id, dataList, dataDetail) => {
  let denormalizedData = null;

  if (dataList) {
    const denormalizedDataList = denormalize(dataList.result, battlesSchema, dataList.entities);

    denormalizedDataList.map((dataList) => {
      if (String(dataList.id) === id) {
        denormalizedData = dataList;
      }
      return denormalizedData;
    });
  } else {
    denormalizedData = denormalize(dataDetail.result, battleSchema, dataDetail.entities);
  }
  return denormalizedData;
};
