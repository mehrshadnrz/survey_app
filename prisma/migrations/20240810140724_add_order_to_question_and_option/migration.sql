/*
  Warnings:

  - Made the column `order` on table `Option` required. This step will fail if there are existing NULL values in that column.
  - Made the column `order` on table `Question` required. This step will fail if there are existing NULL values in that column.

*/
-- AlterTable
ALTER TABLE "Option" ALTER COLUMN "order" SET NOT NULL;

-- AlterTable
ALTER TABLE "Question" ALTER COLUMN "order" SET NOT NULL;
