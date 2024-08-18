/*
  Warnings:

  - You are about to drop the column `surveyId` on the `Response` table. All the data in the column will be lost.
  - Made the column `examSessionId` on table `Response` required. This step will fail if there are existing NULL values in that column.

*/
-- DropForeignKey
ALTER TABLE "Response" DROP CONSTRAINT "Response_surveyId_fkey";

-- AlterTable
ALTER TABLE "Response" DROP COLUMN "surveyId",
ALTER COLUMN "examSessionId" SET NOT NULL;
