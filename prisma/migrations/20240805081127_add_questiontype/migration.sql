/*
  Warnings:

  - You are about to drop the column `type` on the `Question` table. All the data in the column will be lost.
  - Added the required column `questionType` to the `Question` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Question" DROP COLUMN "type",
ADD COLUMN     "questionType" "QuestionType" NOT NULL;
