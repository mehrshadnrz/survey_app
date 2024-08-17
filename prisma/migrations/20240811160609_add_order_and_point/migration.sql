/*
  Warnings:

  - The values [TEXT_INPUT,RATING,FILE_UPLOAD,DATE_PICKER] on the enum `QuestionType` will be removed. If these variants are still used in the database, this will fail.

*/
-- AlterEnum
BEGIN;
CREATE TYPE "QuestionType_new" AS ENUM ('MULTIPLE_CHOICE', 'SHORT_TEXT', 'LONG_TEXT', 'PSYCHOLOGY');
ALTER TABLE "Question" ALTER COLUMN "questionType" TYPE "QuestionType_new" USING ("questionType"::text::"QuestionType_new");
ALTER TYPE "QuestionType" RENAME TO "QuestionType_old";
ALTER TYPE "QuestionType_new" RENAME TO "QuestionType";
DROP TYPE "QuestionType_old";
COMMIT;

-- AlterTable
ALTER TABLE "Question" ADD COLUMN     "correctoption" INTEGER,
ALTER COLUMN "correctAnswer" DROP NOT NULL;
